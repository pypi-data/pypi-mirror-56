# copyright 2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-jsonschema Pyramid views for the JSON API of entities."""

import json
import traceback

from pyramid import httpexceptions
from pyramid.view import view_config
import six

from cubicweb import (
    ValidationError,
)
from cubicweb.web import (
    RequestError as _CWRequestError,
)
from .. import (
    CREATION_ROLE,
)
from ..resources import (
    ETypeResource,
    RootResource,
    WorkflowTransitionsResource,
)
from . import (
    describedby,
    entity_from_context,
    json_config,
    json_problem,
    LOG,
    pagination,
    up_link,
)


def _created(request, resource):
    location = request.resource_url(resource)
    request.response.location = location
    request.response.status_code = 201
    mapper = resource.mapper()
    return mapper.serialize()


def _json_body(request):
    """Return the JSON body found in `request` or raise "415 Unsupported Media
    Type".
    """
    exc_type = ValueError if six.PY2 else json.JSONDecodeError
    try:
        return request.json_body
    except exc_type:
        raise httpexceptions.HTTPUnsupportedMediaType()


@view_config(
    route_name='cubicweb-jsonschema.entities',
    context='cubicweb_jsonschema.resources.IRoot',
    request_method='GET',
    decorator=[describedby],
    permission='authenticated',
)
def get_root(context, request):
    """Site root, no data."""
    request.response.status_code = 204
    request.response.content_type = None
    request.response.allow = ['GET']
    return request.response


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context='cubicweb_jsonschema.resources.IEntities',
    request_method='GET',
    decorator=[
        describedby,
        pagination,
        up_link,
    ],
)
def get_entities(context, request):
    """Render multiple entities in JSON format."""
    if context.has_perm('add'):
        request.response.allow = ['GET', 'POST']
    else:
        request.response.allow = ['GET']
    mapper = context.mapper()
    return mapper.serialize(context.rset.entities())


def allow_for_entity(entity):
    """Return a list of HTTP verbs that are Allow-ed for `entity`.
    """
    perm2verb = [
        ('read', 'GET'),
        ('update', 'PUT'),
        ('delete', 'DELETE'),
    ]
    return [v for p, v in perm2verb if entity.cw_has_perm(p)]


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context='cubicweb_jsonschema.resources.IEntity',
    request_method='GET',
    decorator=[
        describedby,
        entity_from_context,
        up_link,
    ],
)
def get_entity(context, request):
    """Render a single entity in JSON format."""
    entity = context.entity
    request.response.allow = allow_for_entity(entity)
    mapper = context.mapper()
    return mapper.serialize()


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context='cubicweb_jsonschema.resources.IEntities',
    request_method='POST',
)
def create_entity(context, request):
    """Create a new entity from JSON data."""
    # TODO In case of validation errors, it'd be better to give a JSON Schema
    # entry as a "pointer", would require selection context to be an
    # ETypeSchemaResource.
    mapper = context.mapper(CREATION_ROLE)
    instance = _json_body(request)
    values = mapper.values(instance)
    entity = request.cw_cnx.create_entity(mapper.etype, **values)
    request.cw_cnx.commit()
    LOG.info('created %s', entity)
    return _created(request, context[entity.eid])


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context='cubicweb_jsonschema.resources.IEntity',
    request_method='PUT',
    decorator=[entity_from_context],
)
def update_entity(context, request):
    """Update an entity from JSON data."""
    entity = context.entity
    mapper = context.mapper()
    instance = _json_body(request)
    edited_props = list(instance)
    values = mapper.values(instance)
    entity.cw_set(**values)
    request.cw_cnx.commit()
    LOG.info('edited attributes "%s" of %s', ', '.join(edited_props), entity)
    request.response.location = request.resource_url(context)
    request.response.status_code = 200
    return mapper.serialize()


@view_config(
    route_name='delete_entity',
    context='cubicweb_jsonschema.resources.IEntity',
    request_method='DELETE',
    decorator=[entity_from_context],
)
def delete_entity(context, request):
    """Delete an entity."""
    entity = context.entity
    entity.cw_delete()
    request.cw_cnx.commit()
    LOG.info('deleted %s', entity)
    request.response.status_code = 204
    request.response.content_type = None
    return request.response


def allow_for_entity_relation(entity, rtype, role):
    eschema = entity.e_schema
    rdef = eschema.rdef(rtype, role)
    perm2verb = [
        ('read', 'GET'),
        ('add', 'POST'),
    ]
    if role == 'subject':
        kwargs = {'fromeid': entity.eid}
    else:
        kwargs = {'toeid': entity.eid}
    return [v for p, v in perm2verb
            if rdef.has_perm(entity._cw, p, **kwargs)]


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context='cubicweb_jsonschema.resources.IRelatedEntities',
    request_method='GET',
    decorator=[
        describedby,
        pagination,
        up_link,
    ],
)
def get_related_entities(context, request):
    """Return a JSON document of entities target of a relationships."""
    entity = context.__parent__.rset.one()
    request.response.allow = allow_for_entity_relation(
        entity, context.rtype, context.role)
    mapper = context.mapper()
    return mapper.serialize(context.rset.entities())


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context='cubicweb_jsonschema.resources.IRelatedEntities',
    request_method='POST',
)
def post_related_entities(context, request):
    """Insert relationships between entity bound to context and targets from
    request's JSON body.
    """
    entity = context.__parent__.rset.one()
    rtype, role = context.rtype, context.role
    vreg = request.registry['cubicweb.registry']
    mapper = vreg['mappers'].select(
        'jsonschema.relation', request.cw_request,
        entity=entity, rtype=rtype, role=role,
        resource=context,
    )
    payload = _json_body(request)
    if not isinstance(payload, dict):
        return json_problem(status=400, detail='expecting an object')
    instance = {rtype: [payload]}
    # Pass "None" as entity because we want to add a relation, not override
    # existing ones.
    values = mapper.values(None, instance)
    entity.cw_set(**values)
    request.cw_cnx.commit()
    target, = values[mapper.orm_rtype]
    # Depending to whether the relation is inlined or not we might get an
    # entity or and eid.
    eid = getattr(target, 'eid', target)
    try:
        related = context[eid]
    except KeyError:
        # Target may not be reachable through the "related" path as there's no
        # guarantee about this after commit() (e.g. hooks may update data).
        # We thus don't know what to return, hence a 204 No Content.
        request.response.status_code = 204
        request.response.content_type = None
        return request.response
    return _created(request, related)


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context='cubicweb_jsonschema.resources.IRelatedEntity',
    request_method='GET',
    decorator=[
        describedby,
        up_link,
    ],
)
def get_related_entity(context, request):
    """Return a JSON document of an entity target of a relationship."""
    mapper = context.mapper()
    request.response.allow = allow_for_entity(context.entity)
    return mapper.serialize()


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context='cubicweb_jsonschema.resources.IRelatedEntity',
    request_method='PUT',
)
def update_related_entity(context, request):
    """Update a related entity from JSON data."""
    mapper = context.mapper()
    instance = _json_body(request)
    edited_props = list(instance)
    values = mapper.values(instance)
    entity = context.entity
    entity.cw_set(**values)
    request.cw_cnx.commit()
    LOG.info('edited attributes "%s" of %s', ', '.join(edited_props), entity)
    request.response.status_code = 200
    request.response.location = request.resource_url(context)
    return mapper.serialize()


@view_config(
    route_name='delete_entity',
    context='cubicweb_jsonschema.resources.IRelatedEntity',
    request_method='DELETE',
)
def delete_relation(context, request):
    """Delete a relationship."""
    assert context.role == 'subject', 'can only delete subject relation'
    subj = context.__parent__.__parent__.rset.one()
    obj = context.entity
    request.cw_cnx.execute(
        'DELETE S {rtype} O WHERE S eid %(s)s, O eid %(o)s'.format(
            rtype=context.rtype),
        {'s': subj.eid, 'o': obj.eid})
    request.cw_cnx.commit()
    LOG.info('deleted <%s %s %s>', subj, context.rtype, obj)
    request.response.status_code = 204
    request.response.content_type = None
    return request.response


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context=WorkflowTransitionsResource,
    request_method='GET',
    decorator=[
        describedby,
        up_link,
    ],
)
def get_entity_workflow_transitions(context, request):
    """Return a JSON document of workflow transitions of an entity."""
    mapper = context.mapper()
    return mapper.serialize()


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context=WorkflowTransitionsResource,
    request_method='POST',
)
def post_entity_workflow_transition(context, request):
    """Pass a workflow transition for an entity."""
    payload = _json_body(request)
    trname = payload['name']
    comment = payload.get('comment')
    wfobj = context.for_entity.cw_adapt_to('IWorkflowable')
    wfobj.fire_transition(trname, comment=comment)
    request.cw_cnx.commit()
    request.response.status_code = 204
    request.response.content_type = None
    return request.response


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context=ValidationError,
    # This view should be usable for unauthenticated users.
    permission=None,
)
def validation_failed(exc, request):
    """Exception view for ValidationError on JSON request."""
    LOG.info('%s encountered during processing of %s', exc, request)
    _ = request.cw_request._
    request.cw_cnx.rollback()
    exc.translate(_)
    invalid_params = []
    detail = []
    for rolename, value in exc.errors.items():
        if rolename:
            invalid_params.append({'name': rolename, 'reason': value})
        else:
            detail.append(value)
    kwargs = {}
    if detail:
        kwargs['detail'] = '\n'.join(detail)
    if invalid_params:
        kwargs['invalid-params'] = invalid_params
    return json_problem(status=422, **kwargs)


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context=_CWRequestError,
    # This view should be usable for unauthenticated users.
    permission=None,
)
def cubicweb_requesterror(exc, request):
    """Handler for CubicWeb's RequestError instances.

    It will return a RFC 7807 formatted error response from exception found in
    context.

    This view breaks backward-compatibility with CubicWeb's behaviour without
    cubicweb-jsonschema as the JSON response returned by CubicWeb is not
    application/problem+json.
    """
    if request.cw_cnx is not None:
        request.cw_cnx.rollback()
    return json_problem(status=int(exc.status), detail=str(exc))


@json_config(
    route_name='cubicweb-jsonschema.entities',
    context=Exception,
    # This view should be usable for unauthenticated users.
    permission=None,
)
def generic_error(exc, request):
    """Generic exception handler for exception (usually during "edition"
    operations).

    It will return a RFC 7807 formatted error response from exception found in
    context.
    """
    # Because this handler is wired on the "Exception" context, any error will
    # be catched, including the standard pyramid return exceptions.
    # In this case, just return it
    if isinstance(exc, httpexceptions.HTTPException):
        return exc
    if request.cw_cnx is not None:
        request.cw_cnx.rollback()
    LOG.exception('exception occurred while processing %s', request)
    detail = None
    cwconfig = request.registry['cubicweb.config']
    if cwconfig.debugmode or cwconfig.mode == 'test':
        detail = ''.join(
            traceback.format_exception_only(type(exc), exc)
        ).strip()
    return json_problem(status=500, detail=detail)


def includeme(config):
    config.include('cubicweb.pyramid.predicates')
    config.include('..predicates')
    config.add_route('delete_entity', '/{etype}/*traverse',
                     factory=ETypeResource.from_match('etype'),
                     request_method='DELETE',
                     match_is_etype='etype')
    config.add_route(
        'cubicweb-jsonschema.entities',
        '*traverse',
        factory=RootResource,
        strict_accept='application/json',
    )
    config.scan(__name__)
