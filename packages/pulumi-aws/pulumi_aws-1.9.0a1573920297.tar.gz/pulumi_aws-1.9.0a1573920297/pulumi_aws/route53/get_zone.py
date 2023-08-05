# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetZoneResult:
    """
    A collection of values returned by getZone.
    """
    def __init__(__self__, caller_reference=None, comment=None, linked_service_description=None, linked_service_principal=None, name=None, name_servers=None, private_zone=None, resource_record_set_count=None, tags=None, vpc_id=None, zone_id=None, id=None):
        if caller_reference and not isinstance(caller_reference, str):
            raise TypeError("Expected argument 'caller_reference' to be a str")
        __self__.caller_reference = caller_reference
        """
        Caller Reference of the Hosted Zone.
        """
        if comment and not isinstance(comment, str):
            raise TypeError("Expected argument 'comment' to be a str")
        __self__.comment = comment
        """
        The comment field of the Hosted Zone.
        """
        if linked_service_description and not isinstance(linked_service_description, str):
            raise TypeError("Expected argument 'linked_service_description' to be a str")
        __self__.linked_service_description = linked_service_description
        """
        The description provided by the service that created the Hosted Zone (e.g. `arn:aws:servicediscovery:us-east-1:1234567890:namespace/ns-xxxxxxxxxxxxxxxx`).
        """
        if linked_service_principal and not isinstance(linked_service_principal, str):
            raise TypeError("Expected argument 'linked_service_principal' to be a str")
        __self__.linked_service_principal = linked_service_principal
        """
        The service that created the Hosted Zone (e.g. `servicediscovery.amazonaws.com`).
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if name_servers and not isinstance(name_servers, list):
            raise TypeError("Expected argument 'name_servers' to be a list")
        __self__.name_servers = name_servers
        """
        The list of DNS name servers for the Hosted Zone.
        """
        if private_zone and not isinstance(private_zone, bool):
            raise TypeError("Expected argument 'private_zone' to be a bool")
        __self__.private_zone = private_zone
        if resource_record_set_count and not isinstance(resource_record_set_count, float):
            raise TypeError("Expected argument 'resource_record_set_count' to be a float")
        __self__.resource_record_set_count = resource_record_set_count
        """
        The number of Record Set in the Hosted Zone.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        if vpc_id and not isinstance(vpc_id, str):
            raise TypeError("Expected argument 'vpc_id' to be a str")
        __self__.vpc_id = vpc_id
        if zone_id and not isinstance(zone_id, str):
            raise TypeError("Expected argument 'zone_id' to be a str")
        __self__.zone_id = zone_id
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """
class AwaitableGetZoneResult(GetZoneResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetZoneResult(
            caller_reference=self.caller_reference,
            comment=self.comment,
            linked_service_description=self.linked_service_description,
            linked_service_principal=self.linked_service_principal,
            name=self.name,
            name_servers=self.name_servers,
            private_zone=self.private_zone,
            resource_record_set_count=self.resource_record_set_count,
            tags=self.tags,
            vpc_id=self.vpc_id,
            zone_id=self.zone_id,
            id=self.id)

def get_zone(name=None,private_zone=None,resource_record_set_count=None,tags=None,vpc_id=None,zone_id=None,opts=None):
    """
    `route53.Zone` provides details about a specific Route 53 Hosted Zone.
    
    This data source allows to find a Hosted Zone ID given Hosted Zone name and certain search criteria.
    
    :param str name: The Hosted Zone name of the desired Hosted Zone.
    :param bool private_zone: Used with `name` field to get a private Hosted Zone.
    :param dict tags: Used with `name` field. A mapping of tags, each pair of which must exactly match
           a pair on the desired Hosted Zone.
    :param str vpc_id: Used with `name` field to get a private Hosted Zone associated with the vpc_id (in this case, private_zone is not mandatory).
    :param str zone_id: The Hosted Zone id of the desired Hosted Zone.

    > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/d/route53_zone.html.markdown.
    """
    __args__ = dict()

    __args__['name'] = name
    __args__['privateZone'] = private_zone
    __args__['resourceRecordSetCount'] = resource_record_set_count
    __args__['tags'] = tags
    __args__['vpcId'] = vpc_id
    __args__['zoneId'] = zone_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:route53/getZone:getZone', __args__, opts=opts).value

    return AwaitableGetZoneResult(
        caller_reference=__ret__.get('callerReference'),
        comment=__ret__.get('comment'),
        linked_service_description=__ret__.get('linkedServiceDescription'),
        linked_service_principal=__ret__.get('linkedServicePrincipal'),
        name=__ret__.get('name'),
        name_servers=__ret__.get('nameServers'),
        private_zone=__ret__.get('privateZone'),
        resource_record_set_count=__ret__.get('resourceRecordSetCount'),
        tags=__ret__.get('tags'),
        vpc_id=__ret__.get('vpcId'),
        zone_id=__ret__.get('zoneId'),
        id=__ret__.get('id'))
