# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class LoadBalancerBackendServerPolicy(pulumi.CustomResource):
    instance_port: pulumi.Output[float]
    """
    The instance port to apply the policy to.
    """
    load_balancer_name: pulumi.Output[str]
    """
    The load balancer to attach the policy to.
    """
    policy_names: pulumi.Output[list]
    """
    List of Policy Names to apply to the backend server.
    """
    def __init__(__self__, resource_name, opts=None, instance_port=None, load_balancer_name=None, policy_names=None, __props__=None, __name__=None, __opts__=None):
        """
        Attaches a load balancer policy to an ELB backend server.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] instance_port: The instance port to apply the policy to.
        :param pulumi.Input[str] load_balancer_name: The load balancer to attach the policy to.
        :param pulumi.Input[list] policy_names: List of Policy Names to apply to the backend server.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/load_balancer_backend_server_policy.html.markdown.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            if instance_port is None:
                raise TypeError("Missing required property 'instance_port'")
            __props__['instance_port'] = instance_port
            if load_balancer_name is None:
                raise TypeError("Missing required property 'load_balancer_name'")
            __props__['load_balancer_name'] = load_balancer_name
            __props__['policy_names'] = policy_names
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="aws:elasticloadbalancing/loadBalancerBackendServerPolicy:LoadBalancerBackendServerPolicy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(LoadBalancerBackendServerPolicy, __self__).__init__(
            'aws:elb/loadBalancerBackendServerPolicy:LoadBalancerBackendServerPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, instance_port=None, load_balancer_name=None, policy_names=None):
        """
        Get an existing LoadBalancerBackendServerPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] instance_port: The instance port to apply the policy to.
        :param pulumi.Input[str] load_balancer_name: The load balancer to attach the policy to.
        :param pulumi.Input[list] policy_names: List of Policy Names to apply to the backend server.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/load_balancer_backend_server_policy.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["instance_port"] = instance_port
        __props__["load_balancer_name"] = load_balancer_name
        __props__["policy_names"] = policy_names
        return LoadBalancerBackendServerPolicy(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

