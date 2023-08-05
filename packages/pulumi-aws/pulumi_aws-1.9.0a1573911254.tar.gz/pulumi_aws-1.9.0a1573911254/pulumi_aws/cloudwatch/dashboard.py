# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Dashboard(pulumi.CustomResource):
    dashboard_arn: pulumi.Output[str]
    """
    The Amazon Resource Name (ARN) of the dashboard.
    """
    dashboard_body: pulumi.Output[str]
    """
    The detailed information about the dashboard, including what widgets are included and their location on the dashboard. You can read more about the body structure in the [documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/CloudWatch-Dashboard-Body-Structure.html).
    """
    dashboard_name: pulumi.Output[str]
    """
    The name of the dashboard.
    """
    def __init__(__self__, resource_name, opts=None, dashboard_body=None, dashboard_name=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a CloudWatch Dashboard resource.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dashboard_body: The detailed information about the dashboard, including what widgets are included and their location on the dashboard. You can read more about the body structure in the [documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/CloudWatch-Dashboard-Body-Structure.html).
        :param pulumi.Input[str] dashboard_name: The name of the dashboard.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/cloudwatch_dashboard.html.markdown.
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

            if dashboard_body is None:
                raise TypeError("Missing required property 'dashboard_body'")
            __props__['dashboard_body'] = dashboard_body
            if dashboard_name is None:
                raise TypeError("Missing required property 'dashboard_name'")
            __props__['dashboard_name'] = dashboard_name
            __props__['dashboard_arn'] = None
        super(Dashboard, __self__).__init__(
            'aws:cloudwatch/dashboard:Dashboard',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, dashboard_arn=None, dashboard_body=None, dashboard_name=None):
        """
        Get an existing Dashboard resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dashboard_arn: The Amazon Resource Name (ARN) of the dashboard.
        :param pulumi.Input[str] dashboard_body: The detailed information about the dashboard, including what widgets are included and their location on the dashboard. You can read more about the body structure in the [documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/CloudWatch-Dashboard-Body-Structure.html).
        :param pulumi.Input[str] dashboard_name: The name of the dashboard.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/cloudwatch_dashboard.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["dashboard_arn"] = dashboard_arn
        __props__["dashboard_body"] = dashboard_body
        __props__["dashboard_name"] = dashboard_name
        return Dashboard(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

