"Main interface for appsync type defs"
from __future__ import annotations

from typing import Dict, List
from typing_extensions import TypedDict


__all__ = (
    "ClientCreateApiCacheResponseapiCacheTypeDef",
    "ClientCreateApiCacheResponseTypeDef",
    "ClientCreateApiKeyResponseapiKeyTypeDef",
    "ClientCreateApiKeyResponseTypeDef",
    "ClientCreateDataSourceResponsedataSourcedynamodbConfigdeltaSyncConfigTypeDef",
    "ClientCreateDataSourceResponsedataSourcedynamodbConfigTypeDef",
    "ClientCreateDataSourceResponsedataSourceelasticsearchConfigTypeDef",
    "ClientCreateDataSourceResponsedataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef",
    "ClientCreateDataSourceResponsedataSourcehttpConfigauthorizationConfigTypeDef",
    "ClientCreateDataSourceResponsedataSourcehttpConfigTypeDef",
    "ClientCreateDataSourceResponsedataSourcelambdaConfigTypeDef",
    "ClientCreateDataSourceResponsedataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef",
    "ClientCreateDataSourceResponsedataSourcerelationalDatabaseConfigTypeDef",
    "ClientCreateDataSourceResponsedataSourceTypeDef",
    "ClientCreateDataSourceResponseTypeDef",
    "ClientCreateDataSourcedynamodbConfigdeltaSyncConfigTypeDef",
    "ClientCreateDataSourcedynamodbConfigTypeDef",
    "ClientCreateDataSourceelasticsearchConfigTypeDef",
    "ClientCreateDataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef",
    "ClientCreateDataSourcehttpConfigauthorizationConfigTypeDef",
    "ClientCreateDataSourcehttpConfigTypeDef",
    "ClientCreateDataSourcelambdaConfigTypeDef",
    "ClientCreateDataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef",
    "ClientCreateDataSourcerelationalDatabaseConfigTypeDef",
    "ClientCreateFunctionResponsefunctionConfigurationTypeDef",
    "ClientCreateFunctionResponseTypeDef",
    "ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef",
    "ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef",
    "ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersTypeDef",
    "ClientCreateGraphqlApiResponsegraphqlApilogConfigTypeDef",
    "ClientCreateGraphqlApiResponsegraphqlApiopenIDConnectConfigTypeDef",
    "ClientCreateGraphqlApiResponsegraphqlApiuserPoolConfigTypeDef",
    "ClientCreateGraphqlApiResponsegraphqlApiTypeDef",
    "ClientCreateGraphqlApiResponseTypeDef",
    "ClientCreateGraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef",
    "ClientCreateGraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef",
    "ClientCreateGraphqlApiadditionalAuthenticationProvidersTypeDef",
    "ClientCreateGraphqlApilogConfigTypeDef",
    "ClientCreateGraphqlApiopenIDConnectConfigTypeDef",
    "ClientCreateGraphqlApiuserPoolConfigTypeDef",
    "ClientCreateResolverResponseresolvercachingConfigTypeDef",
    "ClientCreateResolverResponseresolverpipelineConfigTypeDef",
    "ClientCreateResolverResponseresolversyncConfiglambdaConflictHandlerConfigTypeDef",
    "ClientCreateResolverResponseresolversyncConfigTypeDef",
    "ClientCreateResolverResponseresolverTypeDef",
    "ClientCreateResolverResponseTypeDef",
    "ClientCreateResolvercachingConfigTypeDef",
    "ClientCreateResolverpipelineConfigTypeDef",
    "ClientCreateResolversyncConfiglambdaConflictHandlerConfigTypeDef",
    "ClientCreateResolversyncConfigTypeDef",
    "ClientCreateTypeResponsetypeTypeDef",
    "ClientCreateTypeResponseTypeDef",
    "ClientGetApiCacheResponseapiCacheTypeDef",
    "ClientGetApiCacheResponseTypeDef",
    "ClientGetDataSourceResponsedataSourcedynamodbConfigdeltaSyncConfigTypeDef",
    "ClientGetDataSourceResponsedataSourcedynamodbConfigTypeDef",
    "ClientGetDataSourceResponsedataSourceelasticsearchConfigTypeDef",
    "ClientGetDataSourceResponsedataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef",
    "ClientGetDataSourceResponsedataSourcehttpConfigauthorizationConfigTypeDef",
    "ClientGetDataSourceResponsedataSourcehttpConfigTypeDef",
    "ClientGetDataSourceResponsedataSourcelambdaConfigTypeDef",
    "ClientGetDataSourceResponsedataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef",
    "ClientGetDataSourceResponsedataSourcerelationalDatabaseConfigTypeDef",
    "ClientGetDataSourceResponsedataSourceTypeDef",
    "ClientGetDataSourceResponseTypeDef",
    "ClientGetFunctionResponsefunctionConfigurationTypeDef",
    "ClientGetFunctionResponseTypeDef",
    "ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef",
    "ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef",
    "ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersTypeDef",
    "ClientGetGraphqlApiResponsegraphqlApilogConfigTypeDef",
    "ClientGetGraphqlApiResponsegraphqlApiopenIDConnectConfigTypeDef",
    "ClientGetGraphqlApiResponsegraphqlApiuserPoolConfigTypeDef",
    "ClientGetGraphqlApiResponsegraphqlApiTypeDef",
    "ClientGetGraphqlApiResponseTypeDef",
    "ClientGetResolverResponseresolvercachingConfigTypeDef",
    "ClientGetResolverResponseresolverpipelineConfigTypeDef",
    "ClientGetResolverResponseresolversyncConfiglambdaConflictHandlerConfigTypeDef",
    "ClientGetResolverResponseresolversyncConfigTypeDef",
    "ClientGetResolverResponseresolverTypeDef",
    "ClientGetResolverResponseTypeDef",
    "ClientGetSchemaCreationStatusResponseTypeDef",
    "ClientGetTypeResponsetypeTypeDef",
    "ClientGetTypeResponseTypeDef",
    "ClientListApiKeysResponseapiKeysTypeDef",
    "ClientListApiKeysResponseTypeDef",
    "ClientListDataSourcesResponsedataSourcesdynamodbConfigdeltaSyncConfigTypeDef",
    "ClientListDataSourcesResponsedataSourcesdynamodbConfigTypeDef",
    "ClientListDataSourcesResponsedataSourceselasticsearchConfigTypeDef",
    "ClientListDataSourcesResponsedataSourceshttpConfigauthorizationConfigawsIamConfigTypeDef",
    "ClientListDataSourcesResponsedataSourceshttpConfigauthorizationConfigTypeDef",
    "ClientListDataSourcesResponsedataSourceshttpConfigTypeDef",
    "ClientListDataSourcesResponsedataSourceslambdaConfigTypeDef",
    "ClientListDataSourcesResponsedataSourcesrelationalDatabaseConfigrdsHttpEndpointConfigTypeDef",
    "ClientListDataSourcesResponsedataSourcesrelationalDatabaseConfigTypeDef",
    "ClientListDataSourcesResponsedataSourcesTypeDef",
    "ClientListDataSourcesResponseTypeDef",
    "ClientListFunctionsResponsefunctionsTypeDef",
    "ClientListFunctionsResponseTypeDef",
    "ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProvidersopenIDConnectConfigTypeDef",
    "ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProvidersuserPoolConfigTypeDef",
    "ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProvidersTypeDef",
    "ClientListGraphqlApisResponsegraphqlApislogConfigTypeDef",
    "ClientListGraphqlApisResponsegraphqlApisopenIDConnectConfigTypeDef",
    "ClientListGraphqlApisResponsegraphqlApisuserPoolConfigTypeDef",
    "ClientListGraphqlApisResponsegraphqlApisTypeDef",
    "ClientListGraphqlApisResponseTypeDef",
    "ClientListResolversByFunctionResponseresolverscachingConfigTypeDef",
    "ClientListResolversByFunctionResponseresolverspipelineConfigTypeDef",
    "ClientListResolversByFunctionResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef",
    "ClientListResolversByFunctionResponseresolverssyncConfigTypeDef",
    "ClientListResolversByFunctionResponseresolversTypeDef",
    "ClientListResolversByFunctionResponseTypeDef",
    "ClientListResolversResponseresolverscachingConfigTypeDef",
    "ClientListResolversResponseresolverspipelineConfigTypeDef",
    "ClientListResolversResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef",
    "ClientListResolversResponseresolverssyncConfigTypeDef",
    "ClientListResolversResponseresolversTypeDef",
    "ClientListResolversResponseTypeDef",
    "ClientListTagsForResourceResponseTypeDef",
    "ClientListTypesResponsetypesTypeDef",
    "ClientListTypesResponseTypeDef",
    "ClientStartSchemaCreationResponseTypeDef",
    "ClientUpdateApiCacheResponseapiCacheTypeDef",
    "ClientUpdateApiCacheResponseTypeDef",
    "ClientUpdateApiKeyResponseapiKeyTypeDef",
    "ClientUpdateApiKeyResponseTypeDef",
    "ClientUpdateDataSourceResponsedataSourcedynamodbConfigdeltaSyncConfigTypeDef",
    "ClientUpdateDataSourceResponsedataSourcedynamodbConfigTypeDef",
    "ClientUpdateDataSourceResponsedataSourceelasticsearchConfigTypeDef",
    "ClientUpdateDataSourceResponsedataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef",
    "ClientUpdateDataSourceResponsedataSourcehttpConfigauthorizationConfigTypeDef",
    "ClientUpdateDataSourceResponsedataSourcehttpConfigTypeDef",
    "ClientUpdateDataSourceResponsedataSourcelambdaConfigTypeDef",
    "ClientUpdateDataSourceResponsedataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef",
    "ClientUpdateDataSourceResponsedataSourcerelationalDatabaseConfigTypeDef",
    "ClientUpdateDataSourceResponsedataSourceTypeDef",
    "ClientUpdateDataSourceResponseTypeDef",
    "ClientUpdateDataSourcedynamodbConfigdeltaSyncConfigTypeDef",
    "ClientUpdateDataSourcedynamodbConfigTypeDef",
    "ClientUpdateDataSourceelasticsearchConfigTypeDef",
    "ClientUpdateDataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef",
    "ClientUpdateDataSourcehttpConfigauthorizationConfigTypeDef",
    "ClientUpdateDataSourcehttpConfigTypeDef",
    "ClientUpdateDataSourcelambdaConfigTypeDef",
    "ClientUpdateDataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef",
    "ClientUpdateDataSourcerelationalDatabaseConfigTypeDef",
    "ClientUpdateFunctionResponsefunctionConfigurationTypeDef",
    "ClientUpdateFunctionResponseTypeDef",
    "ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef",
    "ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef",
    "ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersTypeDef",
    "ClientUpdateGraphqlApiResponsegraphqlApilogConfigTypeDef",
    "ClientUpdateGraphqlApiResponsegraphqlApiopenIDConnectConfigTypeDef",
    "ClientUpdateGraphqlApiResponsegraphqlApiuserPoolConfigTypeDef",
    "ClientUpdateGraphqlApiResponsegraphqlApiTypeDef",
    "ClientUpdateGraphqlApiResponseTypeDef",
    "ClientUpdateGraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef",
    "ClientUpdateGraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef",
    "ClientUpdateGraphqlApiadditionalAuthenticationProvidersTypeDef",
    "ClientUpdateGraphqlApilogConfigTypeDef",
    "ClientUpdateGraphqlApiopenIDConnectConfigTypeDef",
    "ClientUpdateGraphqlApiuserPoolConfigTypeDef",
    "ClientUpdateResolverResponseresolvercachingConfigTypeDef",
    "ClientUpdateResolverResponseresolverpipelineConfigTypeDef",
    "ClientUpdateResolverResponseresolversyncConfiglambdaConflictHandlerConfigTypeDef",
    "ClientUpdateResolverResponseresolversyncConfigTypeDef",
    "ClientUpdateResolverResponseresolverTypeDef",
    "ClientUpdateResolverResponseTypeDef",
    "ClientUpdateResolvercachingConfigTypeDef",
    "ClientUpdateResolverpipelineConfigTypeDef",
    "ClientUpdateResolversyncConfiglambdaConflictHandlerConfigTypeDef",
    "ClientUpdateResolversyncConfigTypeDef",
    "ClientUpdateTypeResponsetypeTypeDef",
    "ClientUpdateTypeResponseTypeDef",
    "ListApiKeysPaginatePaginationConfigTypeDef",
    "ListApiKeysPaginateResponseapiKeysTypeDef",
    "ListApiKeysPaginateResponseTypeDef",
    "ListDataSourcesPaginatePaginationConfigTypeDef",
    "ListDataSourcesPaginateResponsedataSourcesdynamodbConfigdeltaSyncConfigTypeDef",
    "ListDataSourcesPaginateResponsedataSourcesdynamodbConfigTypeDef",
    "ListDataSourcesPaginateResponsedataSourceselasticsearchConfigTypeDef",
    "ListDataSourcesPaginateResponsedataSourceshttpConfigauthorizationConfigawsIamConfigTypeDef",
    "ListDataSourcesPaginateResponsedataSourceshttpConfigauthorizationConfigTypeDef",
    "ListDataSourcesPaginateResponsedataSourceshttpConfigTypeDef",
    "ListDataSourcesPaginateResponsedataSourceslambdaConfigTypeDef",
    "ListDataSourcesPaginateResponsedataSourcesrelationalDatabaseConfigrdsHttpEndpointConfigTypeDef",
    "ListDataSourcesPaginateResponsedataSourcesrelationalDatabaseConfigTypeDef",
    "ListDataSourcesPaginateResponsedataSourcesTypeDef",
    "ListDataSourcesPaginateResponseTypeDef",
    "ListFunctionsPaginatePaginationConfigTypeDef",
    "ListFunctionsPaginateResponsefunctionsTypeDef",
    "ListFunctionsPaginateResponseTypeDef",
    "ListGraphqlApisPaginatePaginationConfigTypeDef",
    "ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProvidersopenIDConnectConfigTypeDef",
    "ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProvidersuserPoolConfigTypeDef",
    "ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProvidersTypeDef",
    "ListGraphqlApisPaginateResponsegraphqlApislogConfigTypeDef",
    "ListGraphqlApisPaginateResponsegraphqlApisopenIDConnectConfigTypeDef",
    "ListGraphqlApisPaginateResponsegraphqlApisuserPoolConfigTypeDef",
    "ListGraphqlApisPaginateResponsegraphqlApisTypeDef",
    "ListGraphqlApisPaginateResponseTypeDef",
    "ListResolversByFunctionPaginatePaginationConfigTypeDef",
    "ListResolversByFunctionPaginateResponseresolverscachingConfigTypeDef",
    "ListResolversByFunctionPaginateResponseresolverspipelineConfigTypeDef",
    "ListResolversByFunctionPaginateResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef",
    "ListResolversByFunctionPaginateResponseresolverssyncConfigTypeDef",
    "ListResolversByFunctionPaginateResponseresolversTypeDef",
    "ListResolversByFunctionPaginateResponseTypeDef",
    "ListResolversPaginatePaginationConfigTypeDef",
    "ListResolversPaginateResponseresolverscachingConfigTypeDef",
    "ListResolversPaginateResponseresolverspipelineConfigTypeDef",
    "ListResolversPaginateResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef",
    "ListResolversPaginateResponseresolverssyncConfigTypeDef",
    "ListResolversPaginateResponseresolversTypeDef",
    "ListResolversPaginateResponseTypeDef",
    "ListTypesPaginatePaginationConfigTypeDef",
    "ListTypesPaginateResponsetypesTypeDef",
    "ListTypesPaginateResponseTypeDef",
)


_ClientCreateApiCacheResponseapiCacheTypeDef = TypedDict(
    "_ClientCreateApiCacheResponseapiCacheTypeDef",
    {
        "ttl": int,
        "apiCachingBehavior": str,
        "transitEncryptionEnabled": bool,
        "atRestEncryptionEnabled": bool,
        "type": str,
        "status": str,
    },
    total=False,
)


class ClientCreateApiCacheResponseapiCacheTypeDef(_ClientCreateApiCacheResponseapiCacheTypeDef):
    """
    Type definition for `ClientCreateApiCacheResponse` `apiCache`

    The ``ApiCache`` object.

    - **ttl** *(integer) --*

      TTL in seconds for cache entries.

      Valid values are between 1 and 3600 seconds.

    - **apiCachingBehavior** *(string) --*

      Caching behavior.

      * **FULL_REQUEST_CACHING** : All requests are fully cached.

      * **PER_RESOLVER_CACHING** : Individual resovlers that you specify are cached.

    - **transitEncryptionEnabled** *(boolean) --*

      Transit encryption flag when connecting to cache. This setting cannot be updated after
      creation.

    - **atRestEncryptionEnabled** *(boolean) --*

      At rest encryption flag for cache. This setting cannot be updated after creation.

    - **type** *(string) --*

      The cache instance type.

      * **T2_SMALL** : A t2.small instance type.

      * **T2_MEDIUM** : A t2.medium instance type.

      * **R4_LARGE** : A r4.large instance type.

      * **R4_XLARGE** : A r4.xlarge instance type.

      * **R4_2XLARGE** : A r4.2xlarge instance type.

      * **R4_4XLARGE** : A r4.4xlarge instance type.

      * **R4_8XLARGE** : A r4.8xlarge instance type.

    - **status** *(string) --*

      The cache instance status.

      * **AVAILABLE** : The instance is available for use.

      * **CREATING** : The instance is currently creating.

      * **DELETING** : The instance is currently deleting.

      * **MODIFYING** : The instance is currently modifying.

      * **FAILED** : The instance has failed creation.
    """


_ClientCreateApiCacheResponseTypeDef = TypedDict(
    "_ClientCreateApiCacheResponseTypeDef",
    {"apiCache": ClientCreateApiCacheResponseapiCacheTypeDef},
    total=False,
)


class ClientCreateApiCacheResponseTypeDef(_ClientCreateApiCacheResponseTypeDef):
    """
    Type definition for `ClientCreateApiCache` `Response`

    Represents the output of a ``CreateApiCache`` operation.

    - **apiCache** *(dict) --*

      The ``ApiCache`` object.

      - **ttl** *(integer) --*

        TTL in seconds for cache entries.

        Valid values are between 1 and 3600 seconds.

      - **apiCachingBehavior** *(string) --*

        Caching behavior.

        * **FULL_REQUEST_CACHING** : All requests are fully cached.

        * **PER_RESOLVER_CACHING** : Individual resovlers that you specify are cached.

      - **transitEncryptionEnabled** *(boolean) --*

        Transit encryption flag when connecting to cache. This setting cannot be updated after
        creation.

      - **atRestEncryptionEnabled** *(boolean) --*

        At rest encryption flag for cache. This setting cannot be updated after creation.

      - **type** *(string) --*

        The cache instance type.

        * **T2_SMALL** : A t2.small instance type.

        * **T2_MEDIUM** : A t2.medium instance type.

        * **R4_LARGE** : A r4.large instance type.

        * **R4_XLARGE** : A r4.xlarge instance type.

        * **R4_2XLARGE** : A r4.2xlarge instance type.

        * **R4_4XLARGE** : A r4.4xlarge instance type.

        * **R4_8XLARGE** : A r4.8xlarge instance type.

      - **status** *(string) --*

        The cache instance status.

        * **AVAILABLE** : The instance is available for use.

        * **CREATING** : The instance is currently creating.

        * **DELETING** : The instance is currently deleting.

        * **MODIFYING** : The instance is currently modifying.

        * **FAILED** : The instance has failed creation.
    """


_ClientCreateApiKeyResponseapiKeyTypeDef = TypedDict(
    "_ClientCreateApiKeyResponseapiKeyTypeDef",
    {"id": str, "description": str, "expires": int},
    total=False,
)


class ClientCreateApiKeyResponseapiKeyTypeDef(_ClientCreateApiKeyResponseapiKeyTypeDef):
    """
    Type definition for `ClientCreateApiKeyResponse` `apiKey`

    The API key.

    - **id** *(string) --*

      The API key ID.

    - **description** *(string) --*

      A description of the purpose of the API key.

    - **expires** *(integer) --*

      The time after which the API key expires. The date is represented as seconds since the epoch,
      rounded down to the nearest hour.
    """


_ClientCreateApiKeyResponseTypeDef = TypedDict(
    "_ClientCreateApiKeyResponseTypeDef",
    {"apiKey": ClientCreateApiKeyResponseapiKeyTypeDef},
    total=False,
)


class ClientCreateApiKeyResponseTypeDef(_ClientCreateApiKeyResponseTypeDef):
    """
    Type definition for `ClientCreateApiKey` `Response`

    - **apiKey** *(dict) --*

      The API key.

      - **id** *(string) --*

        The API key ID.

      - **description** *(string) --*

        A description of the purpose of the API key.

      - **expires** *(integer) --*

        The time after which the API key expires. The date is represented as seconds since the
        epoch, rounded down to the nearest hour.
    """


_ClientCreateDataSourceResponsedataSourcedynamodbConfigdeltaSyncConfigTypeDef = TypedDict(
    "_ClientCreateDataSourceResponsedataSourcedynamodbConfigdeltaSyncConfigTypeDef",
    {"baseTableTTL": int, "deltaSyncTableName": str, "deltaSyncTableTTL": int},
    total=False,
)


class ClientCreateDataSourceResponsedataSourcedynamodbConfigdeltaSyncConfigTypeDef(
    _ClientCreateDataSourceResponsedataSourcedynamodbConfigdeltaSyncConfigTypeDef
):
    """
    Type definition for `ClientCreateDataSourceResponsedataSourcedynamodbConfig` `deltaSyncConfig`

    The ``DeltaSyncConfig`` for a versioned datasource.

    - **baseTableTTL** *(integer) --*

      The number of minutes an Item is stored in the datasource.

    - **deltaSyncTableName** *(string) --*

      The Delta Sync table name.

    - **deltaSyncTableTTL** *(integer) --*

      The number of minutes a Delta Sync log entry is stored in the Delta Sync table.
    """


_ClientCreateDataSourceResponsedataSourcedynamodbConfigTypeDef = TypedDict(
    "_ClientCreateDataSourceResponsedataSourcedynamodbConfigTypeDef",
    {
        "tableName": str,
        "awsRegion": str,
        "useCallerCredentials": bool,
        "deltaSyncConfig": ClientCreateDataSourceResponsedataSourcedynamodbConfigdeltaSyncConfigTypeDef,
        "versioned": bool,
    },
    total=False,
)


class ClientCreateDataSourceResponsedataSourcedynamodbConfigTypeDef(
    _ClientCreateDataSourceResponsedataSourcedynamodbConfigTypeDef
):
    """
    Type definition for `ClientCreateDataSourceResponsedataSource` `dynamodbConfig`

    Amazon DynamoDB settings.

    - **tableName** *(string) --*

      The table name.

    - **awsRegion** *(string) --*

      The AWS Region.

    - **useCallerCredentials** *(boolean) --*

      Set to TRUE to use Amazon Cognito credentials with this data source.

    - **deltaSyncConfig** *(dict) --*

      The ``DeltaSyncConfig`` for a versioned datasource.

      - **baseTableTTL** *(integer) --*

        The number of minutes an Item is stored in the datasource.

      - **deltaSyncTableName** *(string) --*

        The Delta Sync table name.

      - **deltaSyncTableTTL** *(integer) --*

        The number of minutes a Delta Sync log entry is stored in the Delta Sync table.

    - **versioned** *(boolean) --*

      Set to TRUE to use Conflict Detection and Resolution with this data source.
    """


_ClientCreateDataSourceResponsedataSourceelasticsearchConfigTypeDef = TypedDict(
    "_ClientCreateDataSourceResponsedataSourceelasticsearchConfigTypeDef",
    {"endpoint": str, "awsRegion": str},
    total=False,
)


class ClientCreateDataSourceResponsedataSourceelasticsearchConfigTypeDef(
    _ClientCreateDataSourceResponsedataSourceelasticsearchConfigTypeDef
):
    """
    Type definition for `ClientCreateDataSourceResponsedataSource` `elasticsearchConfig`

    Amazon Elasticsearch Service settings.

    - **endpoint** *(string) --*

      The endpoint.

    - **awsRegion** *(string) --*

      The AWS Region.
    """


_ClientCreateDataSourceResponsedataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef = TypedDict(
    "_ClientCreateDataSourceResponsedataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef",
    {"signingRegion": str, "signingServiceName": str},
    total=False,
)


class ClientCreateDataSourceResponsedataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef(
    _ClientCreateDataSourceResponsedataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef
):
    """
    Type definition for `ClientCreateDataSourceResponsedataSourcehttpConfigauthorizationConfig`
    `awsIamConfig`

    The AWS IAM settings.

    - **signingRegion** *(string) --*

      The signing region for AWS IAM authorization.

    - **signingServiceName** *(string) --*

      The signing service name for AWS IAM authorization.
    """


_ClientCreateDataSourceResponsedataSourcehttpConfigauthorizationConfigTypeDef = TypedDict(
    "_ClientCreateDataSourceResponsedataSourcehttpConfigauthorizationConfigTypeDef",
    {
        "authorizationType": str,
        "awsIamConfig": ClientCreateDataSourceResponsedataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef,
    },
    total=False,
)


class ClientCreateDataSourceResponsedataSourcehttpConfigauthorizationConfigTypeDef(
    _ClientCreateDataSourceResponsedataSourcehttpConfigauthorizationConfigTypeDef
):
    """
    Type definition for `ClientCreateDataSourceResponsedataSourcehttpConfig` `authorizationConfig`

    The authorization config in case the HTTP endpoint requires authorization.

    - **authorizationType** *(string) --*

      The authorization type required by the HTTP endpoint.

      * **AWS_IAM** : The authorization type is Sigv4.

    - **awsIamConfig** *(dict) --*

      The AWS IAM settings.

      - **signingRegion** *(string) --*

        The signing region for AWS IAM authorization.

      - **signingServiceName** *(string) --*

        The signing service name for AWS IAM authorization.
    """


_ClientCreateDataSourceResponsedataSourcehttpConfigTypeDef = TypedDict(
    "_ClientCreateDataSourceResponsedataSourcehttpConfigTypeDef",
    {
        "endpoint": str,
        "authorizationConfig": ClientCreateDataSourceResponsedataSourcehttpConfigauthorizationConfigTypeDef,
    },
    total=False,
)


class ClientCreateDataSourceResponsedataSourcehttpConfigTypeDef(
    _ClientCreateDataSourceResponsedataSourcehttpConfigTypeDef
):
    """
    Type definition for `ClientCreateDataSourceResponsedataSource` `httpConfig`

    HTTP endpoint settings.

    - **endpoint** *(string) --*

      The HTTP URL endpoint. You can either specify the domain name or IP, and port combination, and
      the URL scheme must be HTTP or HTTPS. If the port is not specified, AWS AppSync uses the
      default port 80 for the HTTP endpoint and port 443 for HTTPS endpoints.

    - **authorizationConfig** *(dict) --*

      The authorization config in case the HTTP endpoint requires authorization.

      - **authorizationType** *(string) --*

        The authorization type required by the HTTP endpoint.

        * **AWS_IAM** : The authorization type is Sigv4.

      - **awsIamConfig** *(dict) --*

        The AWS IAM settings.

        - **signingRegion** *(string) --*

          The signing region for AWS IAM authorization.

        - **signingServiceName** *(string) --*

          The signing service name for AWS IAM authorization.
    """


_ClientCreateDataSourceResponsedataSourcelambdaConfigTypeDef = TypedDict(
    "_ClientCreateDataSourceResponsedataSourcelambdaConfigTypeDef",
    {"lambdaFunctionArn": str},
    total=False,
)


class ClientCreateDataSourceResponsedataSourcelambdaConfigTypeDef(
    _ClientCreateDataSourceResponsedataSourcelambdaConfigTypeDef
):
    """
    Type definition for `ClientCreateDataSourceResponsedataSource` `lambdaConfig`

    AWS Lambda settings.

    - **lambdaFunctionArn** *(string) --*

      The ARN for the Lambda function.
    """


_ClientCreateDataSourceResponsedataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef = TypedDict(
    "_ClientCreateDataSourceResponsedataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef",
    {
        "awsRegion": str,
        "dbClusterIdentifier": str,
        "databaseName": str,
        "schema": str,
        "awsSecretStoreArn": str,
    },
    total=False,
)


class ClientCreateDataSourceResponsedataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef(
    _ClientCreateDataSourceResponsedataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef
):
    """
    Type definition for `ClientCreateDataSourceResponsedataSourcerelationalDatabaseConfig`
    `rdsHttpEndpointConfig`

    Amazon RDS HTTP endpoint settings.

    - **awsRegion** *(string) --*

      AWS Region for RDS HTTP endpoint.

    - **dbClusterIdentifier** *(string) --*

      Amazon RDS cluster identifier.

    - **databaseName** *(string) --*

      Logical database name.

    - **schema** *(string) --*

      Logical schema name.

    - **awsSecretStoreArn** *(string) --*

      AWS secret store ARN for database credentials.
    """


_ClientCreateDataSourceResponsedataSourcerelationalDatabaseConfigTypeDef = TypedDict(
    "_ClientCreateDataSourceResponsedataSourcerelationalDatabaseConfigTypeDef",
    {
        "relationalDatabaseSourceType": str,
        "rdsHttpEndpointConfig": ClientCreateDataSourceResponsedataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef,
    },
    total=False,
)


class ClientCreateDataSourceResponsedataSourcerelationalDatabaseConfigTypeDef(
    _ClientCreateDataSourceResponsedataSourcerelationalDatabaseConfigTypeDef
):
    """
    Type definition for `ClientCreateDataSourceResponsedataSource` `relationalDatabaseConfig`

    Relational database settings.

    - **relationalDatabaseSourceType** *(string) --*

      Source type for the relational database.

      * **RDS_HTTP_ENDPOINT** : The relational database source type is an Amazon RDS HTTP endpoint.

    - **rdsHttpEndpointConfig** *(dict) --*

      Amazon RDS HTTP endpoint settings.

      - **awsRegion** *(string) --*

        AWS Region for RDS HTTP endpoint.

      - **dbClusterIdentifier** *(string) --*

        Amazon RDS cluster identifier.

      - **databaseName** *(string) --*

        Logical database name.

      - **schema** *(string) --*

        Logical schema name.

      - **awsSecretStoreArn** *(string) --*

        AWS secret store ARN for database credentials.
    """


_ClientCreateDataSourceResponsedataSourceTypeDef = TypedDict(
    "_ClientCreateDataSourceResponsedataSourceTypeDef",
    {
        "dataSourceArn": str,
        "name": str,
        "description": str,
        "type": str,
        "serviceRoleArn": str,
        "dynamodbConfig": ClientCreateDataSourceResponsedataSourcedynamodbConfigTypeDef,
        "lambdaConfig": ClientCreateDataSourceResponsedataSourcelambdaConfigTypeDef,
        "elasticsearchConfig": ClientCreateDataSourceResponsedataSourceelasticsearchConfigTypeDef,
        "httpConfig": ClientCreateDataSourceResponsedataSourcehttpConfigTypeDef,
        "relationalDatabaseConfig": ClientCreateDataSourceResponsedataSourcerelationalDatabaseConfigTypeDef,
    },
    total=False,
)


class ClientCreateDataSourceResponsedataSourceTypeDef(
    _ClientCreateDataSourceResponsedataSourceTypeDef
):
    """
    Type definition for `ClientCreateDataSourceResponse` `dataSource`

    The ``DataSource`` object.

    - **dataSourceArn** *(string) --*

      The data source ARN.

    - **name** *(string) --*

      The name of the data source.

    - **description** *(string) --*

      The description of the data source.

    - **type** *(string) --*

      The type of the data source.

      * **AMAZON_DYNAMODB** : The data source is an Amazon DynamoDB table.

      * **AMAZON_ELASTICSEARCH** : The data source is an Amazon Elasticsearch Service domain.

      * **AWS_LAMBDA** : The data source is an AWS Lambda function.

      * **NONE** : There is no data source. This type is used when you wish to invoke a GraphQL
      operation without connecting to a data source, such as performing data transformation with
      resolvers or triggering a subscription to be invoked from a mutation.

      * **HTTP** : The data source is an HTTP endpoint.

      * **RELATIONAL_DATABASE** : The data source is a relational database.

    - **serviceRoleArn** *(string) --*

      The AWS IAM service role ARN for the data source. The system assumes this role when accessing
      the data source.

    - **dynamodbConfig** *(dict) --*

      Amazon DynamoDB settings.

      - **tableName** *(string) --*

        The table name.

      - **awsRegion** *(string) --*

        The AWS Region.

      - **useCallerCredentials** *(boolean) --*

        Set to TRUE to use Amazon Cognito credentials with this data source.

      - **deltaSyncConfig** *(dict) --*

        The ``DeltaSyncConfig`` for a versioned datasource.

        - **baseTableTTL** *(integer) --*

          The number of minutes an Item is stored in the datasource.

        - **deltaSyncTableName** *(string) --*

          The Delta Sync table name.

        - **deltaSyncTableTTL** *(integer) --*

          The number of minutes a Delta Sync log entry is stored in the Delta Sync table.

      - **versioned** *(boolean) --*

        Set to TRUE to use Conflict Detection and Resolution with this data source.

    - **lambdaConfig** *(dict) --*

      AWS Lambda settings.

      - **lambdaFunctionArn** *(string) --*

        The ARN for the Lambda function.

    - **elasticsearchConfig** *(dict) --*

      Amazon Elasticsearch Service settings.

      - **endpoint** *(string) --*

        The endpoint.

      - **awsRegion** *(string) --*

        The AWS Region.

    - **httpConfig** *(dict) --*

      HTTP endpoint settings.

      - **endpoint** *(string) --*

        The HTTP URL endpoint. You can either specify the domain name or IP, and port combination,
        and the URL scheme must be HTTP or HTTPS. If the port is not specified, AWS AppSync uses the
        default port 80 for the HTTP endpoint and port 443 for HTTPS endpoints.

      - **authorizationConfig** *(dict) --*

        The authorization config in case the HTTP endpoint requires authorization.

        - **authorizationType** *(string) --*

          The authorization type required by the HTTP endpoint.

          * **AWS_IAM** : The authorization type is Sigv4.

        - **awsIamConfig** *(dict) --*

          The AWS IAM settings.

          - **signingRegion** *(string) --*

            The signing region for AWS IAM authorization.

          - **signingServiceName** *(string) --*

            The signing service name for AWS IAM authorization.

    - **relationalDatabaseConfig** *(dict) --*

      Relational database settings.

      - **relationalDatabaseSourceType** *(string) --*

        Source type for the relational database.

        * **RDS_HTTP_ENDPOINT** : The relational database source type is an Amazon RDS HTTP
        endpoint.

      - **rdsHttpEndpointConfig** *(dict) --*

        Amazon RDS HTTP endpoint settings.

        - **awsRegion** *(string) --*

          AWS Region for RDS HTTP endpoint.

        - **dbClusterIdentifier** *(string) --*

          Amazon RDS cluster identifier.

        - **databaseName** *(string) --*

          Logical database name.

        - **schema** *(string) --*

          Logical schema name.

        - **awsSecretStoreArn** *(string) --*

          AWS secret store ARN for database credentials.
    """


_ClientCreateDataSourceResponseTypeDef = TypedDict(
    "_ClientCreateDataSourceResponseTypeDef",
    {"dataSource": ClientCreateDataSourceResponsedataSourceTypeDef},
    total=False,
)


class ClientCreateDataSourceResponseTypeDef(_ClientCreateDataSourceResponseTypeDef):
    """
    Type definition for `ClientCreateDataSource` `Response`

    - **dataSource** *(dict) --*

      The ``DataSource`` object.

      - **dataSourceArn** *(string) --*

        The data source ARN.

      - **name** *(string) --*

        The name of the data source.

      - **description** *(string) --*

        The description of the data source.

      - **type** *(string) --*

        The type of the data source.

        * **AMAZON_DYNAMODB** : The data source is an Amazon DynamoDB table.

        * **AMAZON_ELASTICSEARCH** : The data source is an Amazon Elasticsearch Service domain.

        * **AWS_LAMBDA** : The data source is an AWS Lambda function.

        * **NONE** : There is no data source. This type is used when you wish to invoke a GraphQL
        operation without connecting to a data source, such as performing data transformation with
        resolvers or triggering a subscription to be invoked from a mutation.

        * **HTTP** : The data source is an HTTP endpoint.

        * **RELATIONAL_DATABASE** : The data source is a relational database.

      - **serviceRoleArn** *(string) --*

        The AWS IAM service role ARN for the data source. The system assumes this role when
        accessing the data source.

      - **dynamodbConfig** *(dict) --*

        Amazon DynamoDB settings.

        - **tableName** *(string) --*

          The table name.

        - **awsRegion** *(string) --*

          The AWS Region.

        - **useCallerCredentials** *(boolean) --*

          Set to TRUE to use Amazon Cognito credentials with this data source.

        - **deltaSyncConfig** *(dict) --*

          The ``DeltaSyncConfig`` for a versioned datasource.

          - **baseTableTTL** *(integer) --*

            The number of minutes an Item is stored in the datasource.

          - **deltaSyncTableName** *(string) --*

            The Delta Sync table name.

          - **deltaSyncTableTTL** *(integer) --*

            The number of minutes a Delta Sync log entry is stored in the Delta Sync table.

        - **versioned** *(boolean) --*

          Set to TRUE to use Conflict Detection and Resolution with this data source.

      - **lambdaConfig** *(dict) --*

        AWS Lambda settings.

        - **lambdaFunctionArn** *(string) --*

          The ARN for the Lambda function.

      - **elasticsearchConfig** *(dict) --*

        Amazon Elasticsearch Service settings.

        - **endpoint** *(string) --*

          The endpoint.

        - **awsRegion** *(string) --*

          The AWS Region.

      - **httpConfig** *(dict) --*

        HTTP endpoint settings.

        - **endpoint** *(string) --*

          The HTTP URL endpoint. You can either specify the domain name or IP, and port combination,
          and the URL scheme must be HTTP or HTTPS. If the port is not specified, AWS AppSync uses
          the default port 80 for the HTTP endpoint and port 443 for HTTPS endpoints.

        - **authorizationConfig** *(dict) --*

          The authorization config in case the HTTP endpoint requires authorization.

          - **authorizationType** *(string) --*

            The authorization type required by the HTTP endpoint.

            * **AWS_IAM** : The authorization type is Sigv4.

          - **awsIamConfig** *(dict) --*

            The AWS IAM settings.

            - **signingRegion** *(string) --*

              The signing region for AWS IAM authorization.

            - **signingServiceName** *(string) --*

              The signing service name for AWS IAM authorization.

      - **relationalDatabaseConfig** *(dict) --*

        Relational database settings.

        - **relationalDatabaseSourceType** *(string) --*

          Source type for the relational database.

          * **RDS_HTTP_ENDPOINT** : The relational database source type is an Amazon RDS HTTP
          endpoint.

        - **rdsHttpEndpointConfig** *(dict) --*

          Amazon RDS HTTP endpoint settings.

          - **awsRegion** *(string) --*

            AWS Region for RDS HTTP endpoint.

          - **dbClusterIdentifier** *(string) --*

            Amazon RDS cluster identifier.

          - **databaseName** *(string) --*

            Logical database name.

          - **schema** *(string) --*

            Logical schema name.

          - **awsSecretStoreArn** *(string) --*

            AWS secret store ARN for database credentials.
    """


_ClientCreateDataSourcedynamodbConfigdeltaSyncConfigTypeDef = TypedDict(
    "_ClientCreateDataSourcedynamodbConfigdeltaSyncConfigTypeDef",
    {"baseTableTTL": int, "deltaSyncTableName": str, "deltaSyncTableTTL": int},
    total=False,
)


class ClientCreateDataSourcedynamodbConfigdeltaSyncConfigTypeDef(
    _ClientCreateDataSourcedynamodbConfigdeltaSyncConfigTypeDef
):
    """
    Type definition for `ClientCreateDataSourcedynamodbConfig` `deltaSyncConfig`

    The ``DeltaSyncConfig`` for a versioned datasource.

    - **baseTableTTL** *(integer) --*

      The number of minutes an Item is stored in the datasource.

    - **deltaSyncTableName** *(string) --*

      The Delta Sync table name.

    - **deltaSyncTableTTL** *(integer) --*

      The number of minutes a Delta Sync log entry is stored in the Delta Sync table.
    """


_RequiredClientCreateDataSourcedynamodbConfigTypeDef = TypedDict(
    "_RequiredClientCreateDataSourcedynamodbConfigTypeDef", {"tableName": str, "awsRegion": str}
)
_OptionalClientCreateDataSourcedynamodbConfigTypeDef = TypedDict(
    "_OptionalClientCreateDataSourcedynamodbConfigTypeDef",
    {
        "useCallerCredentials": bool,
        "deltaSyncConfig": ClientCreateDataSourcedynamodbConfigdeltaSyncConfigTypeDef,
        "versioned": bool,
    },
    total=False,
)


class ClientCreateDataSourcedynamodbConfigTypeDef(
    _RequiredClientCreateDataSourcedynamodbConfigTypeDef,
    _OptionalClientCreateDataSourcedynamodbConfigTypeDef,
):
    """
    Type definition for `ClientCreateDataSource` `dynamodbConfig`

    Amazon DynamoDB settings.

    - **tableName** *(string) --* **[REQUIRED]**

      The table name.

    - **awsRegion** *(string) --* **[REQUIRED]**

      The AWS Region.

    - **useCallerCredentials** *(boolean) --*

      Set to TRUE to use Amazon Cognito credentials with this data source.

    - **deltaSyncConfig** *(dict) --*

      The ``DeltaSyncConfig`` for a versioned datasource.

      - **baseTableTTL** *(integer) --*

        The number of minutes an Item is stored in the datasource.

      - **deltaSyncTableName** *(string) --*

        The Delta Sync table name.

      - **deltaSyncTableTTL** *(integer) --*

        The number of minutes a Delta Sync log entry is stored in the Delta Sync table.

    - **versioned** *(boolean) --*

      Set to TRUE to use Conflict Detection and Resolution with this data source.
    """


_ClientCreateDataSourceelasticsearchConfigTypeDef = TypedDict(
    "_ClientCreateDataSourceelasticsearchConfigTypeDef", {"endpoint": str, "awsRegion": str}
)


class ClientCreateDataSourceelasticsearchConfigTypeDef(
    _ClientCreateDataSourceelasticsearchConfigTypeDef
):
    """
    Type definition for `ClientCreateDataSource` `elasticsearchConfig`

    Amazon Elasticsearch Service settings.

    - **endpoint** *(string) --* **[REQUIRED]**

      The endpoint.

    - **awsRegion** *(string) --* **[REQUIRED]**

      The AWS Region.
    """


_ClientCreateDataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef = TypedDict(
    "_ClientCreateDataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef",
    {"signingRegion": str, "signingServiceName": str},
    total=False,
)


class ClientCreateDataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef(
    _ClientCreateDataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef
):
    """
    Type definition for `ClientCreateDataSourcehttpConfigauthorizationConfig` `awsIamConfig`

    The AWS IAM settings.

    - **signingRegion** *(string) --*

      The signing region for AWS IAM authorization.

    - **signingServiceName** *(string) --*

      The signing service name for AWS IAM authorization.
    """


_RequiredClientCreateDataSourcehttpConfigauthorizationConfigTypeDef = TypedDict(
    "_RequiredClientCreateDataSourcehttpConfigauthorizationConfigTypeDef",
    {"authorizationType": str},
)
_OptionalClientCreateDataSourcehttpConfigauthorizationConfigTypeDef = TypedDict(
    "_OptionalClientCreateDataSourcehttpConfigauthorizationConfigTypeDef",
    {"awsIamConfig": ClientCreateDataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef},
    total=False,
)


class ClientCreateDataSourcehttpConfigauthorizationConfigTypeDef(
    _RequiredClientCreateDataSourcehttpConfigauthorizationConfigTypeDef,
    _OptionalClientCreateDataSourcehttpConfigauthorizationConfigTypeDef,
):
    """
    Type definition for `ClientCreateDataSourcehttpConfig` `authorizationConfig`

    The authorization config in case the HTTP endpoint requires authorization.

    - **authorizationType** *(string) --* **[REQUIRED]**

      The authorization type required by the HTTP endpoint.

      * **AWS_IAM** : The authorization type is Sigv4.

    - **awsIamConfig** *(dict) --*

      The AWS IAM settings.

      - **signingRegion** *(string) --*

        The signing region for AWS IAM authorization.

      - **signingServiceName** *(string) --*

        The signing service name for AWS IAM authorization.
    """


_ClientCreateDataSourcehttpConfigTypeDef = TypedDict(
    "_ClientCreateDataSourcehttpConfigTypeDef",
    {
        "endpoint": str,
        "authorizationConfig": ClientCreateDataSourcehttpConfigauthorizationConfigTypeDef,
    },
    total=False,
)


class ClientCreateDataSourcehttpConfigTypeDef(_ClientCreateDataSourcehttpConfigTypeDef):
    """
    Type definition for `ClientCreateDataSource` `httpConfig`

    HTTP endpoint settings.

    - **endpoint** *(string) --*

      The HTTP URL endpoint. You can either specify the domain name or IP, and port combination, and
      the URL scheme must be HTTP or HTTPS. If the port is not specified, AWS AppSync uses the
      default port 80 for the HTTP endpoint and port 443 for HTTPS endpoints.

    - **authorizationConfig** *(dict) --*

      The authorization config in case the HTTP endpoint requires authorization.

      - **authorizationType** *(string) --* **[REQUIRED]**

        The authorization type required by the HTTP endpoint.

        * **AWS_IAM** : The authorization type is Sigv4.

      - **awsIamConfig** *(dict) --*

        The AWS IAM settings.

        - **signingRegion** *(string) --*

          The signing region for AWS IAM authorization.

        - **signingServiceName** *(string) --*

          The signing service name for AWS IAM authorization.
    """


_ClientCreateDataSourcelambdaConfigTypeDef = TypedDict(
    "_ClientCreateDataSourcelambdaConfigTypeDef", {"lambdaFunctionArn": str}
)


class ClientCreateDataSourcelambdaConfigTypeDef(_ClientCreateDataSourcelambdaConfigTypeDef):
    """
    Type definition for `ClientCreateDataSource` `lambdaConfig`

    AWS Lambda settings.

    - **lambdaFunctionArn** *(string) --* **[REQUIRED]**

      The ARN for the Lambda function.
    """


_ClientCreateDataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef = TypedDict(
    "_ClientCreateDataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef",
    {
        "awsRegion": str,
        "dbClusterIdentifier": str,
        "databaseName": str,
        "schema": str,
        "awsSecretStoreArn": str,
    },
    total=False,
)


class ClientCreateDataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef(
    _ClientCreateDataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef
):
    """
    Type definition for `ClientCreateDataSourcerelationalDatabaseConfig` `rdsHttpEndpointConfig`

    Amazon RDS HTTP endpoint settings.

    - **awsRegion** *(string) --*

      AWS Region for RDS HTTP endpoint.

    - **dbClusterIdentifier** *(string) --*

      Amazon RDS cluster identifier.

    - **databaseName** *(string) --*

      Logical database name.

    - **schema** *(string) --*

      Logical schema name.

    - **awsSecretStoreArn** *(string) --*

      AWS secret store ARN for database credentials.
    """


_ClientCreateDataSourcerelationalDatabaseConfigTypeDef = TypedDict(
    "_ClientCreateDataSourcerelationalDatabaseConfigTypeDef",
    {
        "relationalDatabaseSourceType": str,
        "rdsHttpEndpointConfig": ClientCreateDataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef,
    },
    total=False,
)


class ClientCreateDataSourcerelationalDatabaseConfigTypeDef(
    _ClientCreateDataSourcerelationalDatabaseConfigTypeDef
):
    """
    Type definition for `ClientCreateDataSource` `relationalDatabaseConfig`

    Relational database settings.

    - **relationalDatabaseSourceType** *(string) --*

      Source type for the relational database.

      * **RDS_HTTP_ENDPOINT** : The relational database source type is an Amazon RDS HTTP endpoint.

    - **rdsHttpEndpointConfig** *(dict) --*

      Amazon RDS HTTP endpoint settings.

      - **awsRegion** *(string) --*

        AWS Region for RDS HTTP endpoint.

      - **dbClusterIdentifier** *(string) --*

        Amazon RDS cluster identifier.

      - **databaseName** *(string) --*

        Logical database name.

      - **schema** *(string) --*

        Logical schema name.

      - **awsSecretStoreArn** *(string) --*

        AWS secret store ARN for database credentials.
    """


_ClientCreateFunctionResponsefunctionConfigurationTypeDef = TypedDict(
    "_ClientCreateFunctionResponsefunctionConfigurationTypeDef",
    {
        "functionId": str,
        "functionArn": str,
        "name": str,
        "description": str,
        "dataSourceName": str,
        "requestMappingTemplate": str,
        "responseMappingTemplate": str,
        "functionVersion": str,
    },
    total=False,
)


class ClientCreateFunctionResponsefunctionConfigurationTypeDef(
    _ClientCreateFunctionResponsefunctionConfigurationTypeDef
):
    """
    Type definition for `ClientCreateFunctionResponse` `functionConfiguration`

    The ``Function`` object.

    - **functionId** *(string) --*

      A unique ID representing the ``Function`` object.

    - **functionArn** *(string) --*

      The ARN of the ``Function`` object.

    - **name** *(string) --*

      The name of the ``Function`` object.

    - **description** *(string) --*

      The ``Function`` description.

    - **dataSourceName** *(string) --*

      The name of the ``DataSource`` .

    - **requestMappingTemplate** *(string) --*

      The ``Function`` request mapping template. Functions support only the 2018-05-29 version of
      the request mapping template.

    - **responseMappingTemplate** *(string) --*

      The ``Function`` response mapping template.

    - **functionVersion** *(string) --*

      The version of the request mapping template. Currently only the 2018-05-29 version of the
      template is supported.
    """


_ClientCreateFunctionResponseTypeDef = TypedDict(
    "_ClientCreateFunctionResponseTypeDef",
    {"functionConfiguration": ClientCreateFunctionResponsefunctionConfigurationTypeDef},
    total=False,
)


class ClientCreateFunctionResponseTypeDef(_ClientCreateFunctionResponseTypeDef):
    """
    Type definition for `ClientCreateFunction` `Response`

    - **functionConfiguration** *(dict) --*

      The ``Function`` object.

      - **functionId** *(string) --*

        A unique ID representing the ``Function`` object.

      - **functionArn** *(string) --*

        The ARN of the ``Function`` object.

      - **name** *(string) --*

        The name of the ``Function`` object.

      - **description** *(string) --*

        The ``Function`` description.

      - **dataSourceName** *(string) --*

        The name of the ``DataSource`` .

      - **requestMappingTemplate** *(string) --*

        The ``Function`` request mapping template. Functions support only the 2018-05-29 version of
        the request mapping template.

      - **responseMappingTemplate** *(string) --*

        The ``Function`` response mapping template.

      - **functionVersion** *(string) --*

        The version of the request mapping template. Currently only the 2018-05-29 version of the
        template is supported.
    """


_ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef = TypedDict(
    "_ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef",
    {"issuer": str, "clientId": str, "iatTTL": int, "authTTL": int},
    total=False,
)


class ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef(
    _ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef
):
    """
    Type definition for `ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProviders`
    `openIDConnectConfig`

    The OpenID Connect configuration.

    - **issuer** *(string) --*

      The issuer for the OpenID Connect configuration. The issuer returned by discovery must exactly
      match the value of ``iss`` in the ID token.

    - **clientId** *(string) --*

      The client identifier of the Relying party at the OpenID identity provider. This identifier is
      typically obtained when the Relying party is registered with the OpenID identity provider. You
      can specify a regular expression so the AWS AppSync can validate against multiple client
      identifiers at a time.

    - **iatTTL** *(integer) --*

      The number of milliseconds a token is valid after being issued to a user.

    - **authTTL** *(integer) --*

      The number of milliseconds a token is valid after being authenticated.
    """


_ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef = TypedDict(
    "_ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef",
    {"userPoolId": str, "awsRegion": str, "appIdClientRegex": str},
    total=False,
)


class ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef(
    _ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef
):
    """
    Type definition for `ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProviders`
    `userPoolConfig`

    The Amazon Cognito user pool configuration.

    - **userPoolId** *(string) --*

      The user pool ID.

    - **awsRegion** *(string) --*

      The AWS Region in which the user pool was created.

    - **appIdClientRegex** *(string) --*

      A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersTypeDef = TypedDict(
    "_ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersTypeDef",
    {
        "authenticationType": str,
        "openIDConnectConfig": ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef,
        "userPoolConfig": ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef,
    },
    total=False,
)


class ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersTypeDef(
    _ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersTypeDef
):
    """
    Type definition for `ClientCreateGraphqlApiResponsegraphqlApi`
    `additionalAuthenticationProviders`

    Describes an additional authentication provider.

    - **authenticationType** *(string) --*

      The authentication type: API key, AWS IAM, OIDC, or Amazon Cognito user pools.

    - **openIDConnectConfig** *(dict) --*

      The OpenID Connect configuration.

      - **issuer** *(string) --*

        The issuer for the OpenID Connect configuration. The issuer returned by discovery must
        exactly match the value of ``iss`` in the ID token.

      - **clientId** *(string) --*

        The client identifier of the Relying party at the OpenID identity provider. This identifier
        is typically obtained when the Relying party is registered with the OpenID identity
        provider. You can specify a regular expression so the AWS AppSync can validate against
        multiple client identifiers at a time.

      - **iatTTL** *(integer) --*

        The number of milliseconds a token is valid after being issued to a user.

      - **authTTL** *(integer) --*

        The number of milliseconds a token is valid after being authenticated.

    - **userPoolConfig** *(dict) --*

      The Amazon Cognito user pool configuration.

      - **userPoolId** *(string) --*

        The user pool ID.

      - **awsRegion** *(string) --*

        The AWS Region in which the user pool was created.

      - **appIdClientRegex** *(string) --*

        A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientCreateGraphqlApiResponsegraphqlApilogConfigTypeDef = TypedDict(
    "_ClientCreateGraphqlApiResponsegraphqlApilogConfigTypeDef",
    {"fieldLogLevel": str, "cloudWatchLogsRoleArn": str, "excludeVerboseContent": bool},
    total=False,
)


class ClientCreateGraphqlApiResponsegraphqlApilogConfigTypeDef(
    _ClientCreateGraphqlApiResponsegraphqlApilogConfigTypeDef
):
    """
    Type definition for `ClientCreateGraphqlApiResponsegraphqlApi` `logConfig`

    The Amazon CloudWatch Logs configuration.

    - **fieldLogLevel** *(string) --*

      The field logging level. Values can be NONE, ERROR, or ALL.

      * **NONE** : No field-level logs are captured.

      * **ERROR** : Logs the following information only for the fields that are in error:

        * The error section in the server response.

        * Field-level errors.

        * The generated request/response functions that got resolved for error fields.

      * **ALL** : The following information is logged for all fields in the query:

        * Field-level tracing information.

        * The generated request/response functions that got resolved for each field.

    - **cloudWatchLogsRoleArn** *(string) --*

      The service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in your
      account.

    - **excludeVerboseContent** *(boolean) --*

      Set to TRUE to exclude sections that contain information such as headers, context, and
      evaluated mapping templates, regardless of logging level.
    """


_ClientCreateGraphqlApiResponsegraphqlApiopenIDConnectConfigTypeDef = TypedDict(
    "_ClientCreateGraphqlApiResponsegraphqlApiopenIDConnectConfigTypeDef",
    {"issuer": str, "clientId": str, "iatTTL": int, "authTTL": int},
    total=False,
)


class ClientCreateGraphqlApiResponsegraphqlApiopenIDConnectConfigTypeDef(
    _ClientCreateGraphqlApiResponsegraphqlApiopenIDConnectConfigTypeDef
):
    """
    Type definition for `ClientCreateGraphqlApiResponsegraphqlApi` `openIDConnectConfig`

    The OpenID Connect configuration.

    - **issuer** *(string) --*

      The issuer for the OpenID Connect configuration. The issuer returned by discovery must exactly
      match the value of ``iss`` in the ID token.

    - **clientId** *(string) --*

      The client identifier of the Relying party at the OpenID identity provider. This identifier is
      typically obtained when the Relying party is registered with the OpenID identity provider. You
      can specify a regular expression so the AWS AppSync can validate against multiple client
      identifiers at a time.

    - **iatTTL** *(integer) --*

      The number of milliseconds a token is valid after being issued to a user.

    - **authTTL** *(integer) --*

      The number of milliseconds a token is valid after being authenticated.
    """


_ClientCreateGraphqlApiResponsegraphqlApiuserPoolConfigTypeDef = TypedDict(
    "_ClientCreateGraphqlApiResponsegraphqlApiuserPoolConfigTypeDef",
    {"userPoolId": str, "awsRegion": str, "defaultAction": str, "appIdClientRegex": str},
    total=False,
)


class ClientCreateGraphqlApiResponsegraphqlApiuserPoolConfigTypeDef(
    _ClientCreateGraphqlApiResponsegraphqlApiuserPoolConfigTypeDef
):
    """
    Type definition for `ClientCreateGraphqlApiResponsegraphqlApi` `userPoolConfig`

    The Amazon Cognito user pool configuration.

    - **userPoolId** *(string) --*

      The user pool ID.

    - **awsRegion** *(string) --*

      The AWS Region in which the user pool was created.

    - **defaultAction** *(string) --*

      The action that you want your GraphQL API to take when a request that uses Amazon Cognito user
      pool authentication doesn't match the Amazon Cognito user pool configuration.

    - **appIdClientRegex** *(string) --*

      A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientCreateGraphqlApiResponsegraphqlApiTypeDef = TypedDict(
    "_ClientCreateGraphqlApiResponsegraphqlApiTypeDef",
    {
        "name": str,
        "apiId": str,
        "authenticationType": str,
        "logConfig": ClientCreateGraphqlApiResponsegraphqlApilogConfigTypeDef,
        "userPoolConfig": ClientCreateGraphqlApiResponsegraphqlApiuserPoolConfigTypeDef,
        "openIDConnectConfig": ClientCreateGraphqlApiResponsegraphqlApiopenIDConnectConfigTypeDef,
        "arn": str,
        "uris": Dict[str, str],
        "tags": Dict[str, str],
        "additionalAuthenticationProviders": List[
            ClientCreateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersTypeDef
        ],
    },
    total=False,
)


class ClientCreateGraphqlApiResponsegraphqlApiTypeDef(
    _ClientCreateGraphqlApiResponsegraphqlApiTypeDef
):
    """
    Type definition for `ClientCreateGraphqlApiResponse` `graphqlApi`

    The ``GraphqlApi`` .

    - **name** *(string) --*

      The API name.

    - **apiId** *(string) --*

      The API ID.

    - **authenticationType** *(string) --*

      The authentication type.

    - **logConfig** *(dict) --*

      The Amazon CloudWatch Logs configuration.

      - **fieldLogLevel** *(string) --*

        The field logging level. Values can be NONE, ERROR, or ALL.

        * **NONE** : No field-level logs are captured.

        * **ERROR** : Logs the following information only for the fields that are in error:

          * The error section in the server response.

          * Field-level errors.

          * The generated request/response functions that got resolved for error fields.

        * **ALL** : The following information is logged for all fields in the query:

          * Field-level tracing information.

          * The generated request/response functions that got resolved for each field.

      - **cloudWatchLogsRoleArn** *(string) --*

        The service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in your
        account.

      - **excludeVerboseContent** *(boolean) --*

        Set to TRUE to exclude sections that contain information such as headers, context, and
        evaluated mapping templates, regardless of logging level.

    - **userPoolConfig** *(dict) --*

      The Amazon Cognito user pool configuration.

      - **userPoolId** *(string) --*

        The user pool ID.

      - **awsRegion** *(string) --*

        The AWS Region in which the user pool was created.

      - **defaultAction** *(string) --*

        The action that you want your GraphQL API to take when a request that uses Amazon Cognito
        user pool authentication doesn't match the Amazon Cognito user pool configuration.

      - **appIdClientRegex** *(string) --*

        A regular expression for validating the incoming Amazon Cognito user pool app client ID.

    - **openIDConnectConfig** *(dict) --*

      The OpenID Connect configuration.

      - **issuer** *(string) --*

        The issuer for the OpenID Connect configuration. The issuer returned by discovery must
        exactly match the value of ``iss`` in the ID token.

      - **clientId** *(string) --*

        The client identifier of the Relying party at the OpenID identity provider. This identifier
        is typically obtained when the Relying party is registered with the OpenID identity
        provider. You can specify a regular expression so the AWS AppSync can validate against
        multiple client identifiers at a time.

      - **iatTTL** *(integer) --*

        The number of milliseconds a token is valid after being issued to a user.

      - **authTTL** *(integer) --*

        The number of milliseconds a token is valid after being authenticated.

    - **arn** *(string) --*

      The ARN.

    - **uris** *(dict) --*

      The URIs.

      - *(string) --*

        - *(string) --*

    - **tags** *(dict) --*

      The tags.

      - *(string) --*

        The key for the tag.

        - *(string) --*

          The value for the tag.

    - **additionalAuthenticationProviders** *(list) --*

      A list of additional authentication providers for the ``GraphqlApi`` API.

      - *(dict) --*

        Describes an additional authentication provider.

        - **authenticationType** *(string) --*

          The authentication type: API key, AWS IAM, OIDC, or Amazon Cognito user pools.

        - **openIDConnectConfig** *(dict) --*

          The OpenID Connect configuration.

          - **issuer** *(string) --*

            The issuer for the OpenID Connect configuration. The issuer returned by discovery must
            exactly match the value of ``iss`` in the ID token.

          - **clientId** *(string) --*

            The client identifier of the Relying party at the OpenID identity provider. This
            identifier is typically obtained when the Relying party is registered with the OpenID
            identity provider. You can specify a regular expression so the AWS AppSync can validate
            against multiple client identifiers at a time.

          - **iatTTL** *(integer) --*

            The number of milliseconds a token is valid after being issued to a user.

          - **authTTL** *(integer) --*

            The number of milliseconds a token is valid after being authenticated.

        - **userPoolConfig** *(dict) --*

          The Amazon Cognito user pool configuration.

          - **userPoolId** *(string) --*

            The user pool ID.

          - **awsRegion** *(string) --*

            The AWS Region in which the user pool was created.

          - **appIdClientRegex** *(string) --*

            A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientCreateGraphqlApiResponseTypeDef = TypedDict(
    "_ClientCreateGraphqlApiResponseTypeDef",
    {"graphqlApi": ClientCreateGraphqlApiResponsegraphqlApiTypeDef},
    total=False,
)


class ClientCreateGraphqlApiResponseTypeDef(_ClientCreateGraphqlApiResponseTypeDef):
    """
    Type definition for `ClientCreateGraphqlApi` `Response`

    - **graphqlApi** *(dict) --*

      The ``GraphqlApi`` .

      - **name** *(string) --*

        The API name.

      - **apiId** *(string) --*

        The API ID.

      - **authenticationType** *(string) --*

        The authentication type.

      - **logConfig** *(dict) --*

        The Amazon CloudWatch Logs configuration.

        - **fieldLogLevel** *(string) --*

          The field logging level. Values can be NONE, ERROR, or ALL.

          * **NONE** : No field-level logs are captured.

          * **ERROR** : Logs the following information only for the fields that are in error:

            * The error section in the server response.

            * Field-level errors.

            * The generated request/response functions that got resolved for error fields.

          * **ALL** : The following information is logged for all fields in the query:

            * Field-level tracing information.

            * The generated request/response functions that got resolved for each field.

        - **cloudWatchLogsRoleArn** *(string) --*

          The service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in your
          account.

        - **excludeVerboseContent** *(boolean) --*

          Set to TRUE to exclude sections that contain information such as headers, context, and
          evaluated mapping templates, regardless of logging level.

      - **userPoolConfig** *(dict) --*

        The Amazon Cognito user pool configuration.

        - **userPoolId** *(string) --*

          The user pool ID.

        - **awsRegion** *(string) --*

          The AWS Region in which the user pool was created.

        - **defaultAction** *(string) --*

          The action that you want your GraphQL API to take when a request that uses Amazon Cognito
          user pool authentication doesn't match the Amazon Cognito user pool configuration.

        - **appIdClientRegex** *(string) --*

          A regular expression for validating the incoming Amazon Cognito user pool app client ID.

      - **openIDConnectConfig** *(dict) --*

        The OpenID Connect configuration.

        - **issuer** *(string) --*

          The issuer for the OpenID Connect configuration. The issuer returned by discovery must
          exactly match the value of ``iss`` in the ID token.

        - **clientId** *(string) --*

          The client identifier of the Relying party at the OpenID identity provider. This
          identifier is typically obtained when the Relying party is registered with the OpenID
          identity provider. You can specify a regular expression so the AWS AppSync can validate
          against multiple client identifiers at a time.

        - **iatTTL** *(integer) --*

          The number of milliseconds a token is valid after being issued to a user.

        - **authTTL** *(integer) --*

          The number of milliseconds a token is valid after being authenticated.

      - **arn** *(string) --*

        The ARN.

      - **uris** *(dict) --*

        The URIs.

        - *(string) --*

          - *(string) --*

      - **tags** *(dict) --*

        The tags.

        - *(string) --*

          The key for the tag.

          - *(string) --*

            The value for the tag.

      - **additionalAuthenticationProviders** *(list) --*

        A list of additional authentication providers for the ``GraphqlApi`` API.

        - *(dict) --*

          Describes an additional authentication provider.

          - **authenticationType** *(string) --*

            The authentication type: API key, AWS IAM, OIDC, or Amazon Cognito user pools.

          - **openIDConnectConfig** *(dict) --*

            The OpenID Connect configuration.

            - **issuer** *(string) --*

              The issuer for the OpenID Connect configuration. The issuer returned by discovery must
              exactly match the value of ``iss`` in the ID token.

            - **clientId** *(string) --*

              The client identifier of the Relying party at the OpenID identity provider. This
              identifier is typically obtained when the Relying party is registered with the OpenID
              identity provider. You can specify a regular expression so the AWS AppSync can
              validate against multiple client identifiers at a time.

            - **iatTTL** *(integer) --*

              The number of milliseconds a token is valid after being issued to a user.

            - **authTTL** *(integer) --*

              The number of milliseconds a token is valid after being authenticated.

          - **userPoolConfig** *(dict) --*

            The Amazon Cognito user pool configuration.

            - **userPoolId** *(string) --*

              The user pool ID.

            - **awsRegion** *(string) --*

              The AWS Region in which the user pool was created.

            - **appIdClientRegex** *(string) --*

              A regular expression for validating the incoming Amazon Cognito user pool app client
              ID.
    """


_RequiredClientCreateGraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef = TypedDict(
    "_RequiredClientCreateGraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef",
    {"issuer": str},
)
_OptionalClientCreateGraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef = TypedDict(
    "_OptionalClientCreateGraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef",
    {"clientId": str, "iatTTL": int, "authTTL": int},
    total=False,
)


class ClientCreateGraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef(
    _RequiredClientCreateGraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef,
    _OptionalClientCreateGraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef,
):
    """
    Type definition for `ClientCreateGraphqlApiadditionalAuthenticationProviders`
    `openIDConnectConfig`

    The OpenID Connect configuration.

    - **issuer** *(string) --* **[REQUIRED]**

      The issuer for the OpenID Connect configuration. The issuer returned by discovery must exactly
      match the value of ``iss`` in the ID token.

    - **clientId** *(string) --*

      The client identifier of the Relying party at the OpenID identity provider. This identifier is
      typically obtained when the Relying party is registered with the OpenID identity provider. You
      can specify a regular expression so the AWS AppSync can validate against multiple client
      identifiers at a time.

    - **iatTTL** *(integer) --*

      The number of milliseconds a token is valid after being issued to a user.

    - **authTTL** *(integer) --*

      The number of milliseconds a token is valid after being authenticated.
    """


_RequiredClientCreateGraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef = TypedDict(
    "_RequiredClientCreateGraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef",
    {"userPoolId": str, "awsRegion": str},
)
_OptionalClientCreateGraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef = TypedDict(
    "_OptionalClientCreateGraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef",
    {"appIdClientRegex": str},
    total=False,
)


class ClientCreateGraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef(
    _RequiredClientCreateGraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef,
    _OptionalClientCreateGraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef,
):
    """
    Type definition for `ClientCreateGraphqlApiadditionalAuthenticationProviders` `userPoolConfig`

    The Amazon Cognito user pool configuration.

    - **userPoolId** *(string) --* **[REQUIRED]**

      The user pool ID.

    - **awsRegion** *(string) --* **[REQUIRED]**

      The AWS Region in which the user pool was created.

    - **appIdClientRegex** *(string) --*

      A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientCreateGraphqlApiadditionalAuthenticationProvidersTypeDef = TypedDict(
    "_ClientCreateGraphqlApiadditionalAuthenticationProvidersTypeDef",
    {
        "authenticationType": str,
        "openIDConnectConfig": ClientCreateGraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef,
        "userPoolConfig": ClientCreateGraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef,
    },
    total=False,
)


class ClientCreateGraphqlApiadditionalAuthenticationProvidersTypeDef(
    _ClientCreateGraphqlApiadditionalAuthenticationProvidersTypeDef
):
    """
    Type definition for `ClientCreateGraphqlApi` `additionalAuthenticationProviders`

    Describes an additional authentication provider.

    - **authenticationType** *(string) --*

      The authentication type: API key, AWS IAM, OIDC, or Amazon Cognito user pools.

    - **openIDConnectConfig** *(dict) --*

      The OpenID Connect configuration.

      - **issuer** *(string) --* **[REQUIRED]**

        The issuer for the OpenID Connect configuration. The issuer returned by discovery must
        exactly match the value of ``iss`` in the ID token.

      - **clientId** *(string) --*

        The client identifier of the Relying party at the OpenID identity provider. This identifier
        is typically obtained when the Relying party is registered with the OpenID identity
        provider. You can specify a regular expression so the AWS AppSync can validate against
        multiple client identifiers at a time.

      - **iatTTL** *(integer) --*

        The number of milliseconds a token is valid after being issued to a user.

      - **authTTL** *(integer) --*

        The number of milliseconds a token is valid after being authenticated.

    - **userPoolConfig** *(dict) --*

      The Amazon Cognito user pool configuration.

      - **userPoolId** *(string) --* **[REQUIRED]**

        The user pool ID.

      - **awsRegion** *(string) --* **[REQUIRED]**

        The AWS Region in which the user pool was created.

      - **appIdClientRegex** *(string) --*

        A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_RequiredClientCreateGraphqlApilogConfigTypeDef = TypedDict(
    "_RequiredClientCreateGraphqlApilogConfigTypeDef",
    {"fieldLogLevel": str, "cloudWatchLogsRoleArn": str},
)
_OptionalClientCreateGraphqlApilogConfigTypeDef = TypedDict(
    "_OptionalClientCreateGraphqlApilogConfigTypeDef", {"excludeVerboseContent": bool}, total=False
)


class ClientCreateGraphqlApilogConfigTypeDef(
    _RequiredClientCreateGraphqlApilogConfigTypeDef, _OptionalClientCreateGraphqlApilogConfigTypeDef
):
    """
    Type definition for `ClientCreateGraphqlApi` `logConfig`

    The Amazon CloudWatch Logs configuration.

    - **fieldLogLevel** *(string) --* **[REQUIRED]**

      The field logging level. Values can be NONE, ERROR, or ALL.

      * **NONE** : No field-level logs are captured.

      * **ERROR** : Logs the following information only for the fields that are in error:

        * The error section in the server response.

        * Field-level errors.

        * The generated request/response functions that got resolved for error fields.

      * **ALL** : The following information is logged for all fields in the query:

        * Field-level tracing information.

        * The generated request/response functions that got resolved for each field.

    - **cloudWatchLogsRoleArn** *(string) --* **[REQUIRED]**

      The service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in your
      account.

    - **excludeVerboseContent** *(boolean) --*

      Set to TRUE to exclude sections that contain information such as headers, context, and
      evaluated mapping templates, regardless of logging level.
    """


_RequiredClientCreateGraphqlApiopenIDConnectConfigTypeDef = TypedDict(
    "_RequiredClientCreateGraphqlApiopenIDConnectConfigTypeDef", {"issuer": str}
)
_OptionalClientCreateGraphqlApiopenIDConnectConfigTypeDef = TypedDict(
    "_OptionalClientCreateGraphqlApiopenIDConnectConfigTypeDef",
    {"clientId": str, "iatTTL": int, "authTTL": int},
    total=False,
)


class ClientCreateGraphqlApiopenIDConnectConfigTypeDef(
    _RequiredClientCreateGraphqlApiopenIDConnectConfigTypeDef,
    _OptionalClientCreateGraphqlApiopenIDConnectConfigTypeDef,
):
    """
    Type definition for `ClientCreateGraphqlApi` `openIDConnectConfig`

    The OpenID Connect configuration.

    - **issuer** *(string) --* **[REQUIRED]**

      The issuer for the OpenID Connect configuration. The issuer returned by discovery must exactly
      match the value of ``iss`` in the ID token.

    - **clientId** *(string) --*

      The client identifier of the Relying party at the OpenID identity provider. This identifier is
      typically obtained when the Relying party is registered with the OpenID identity provider. You
      can specify a regular expression so the AWS AppSync can validate against multiple client
      identifiers at a time.

    - **iatTTL** *(integer) --*

      The number of milliseconds a token is valid after being issued to a user.

    - **authTTL** *(integer) --*

      The number of milliseconds a token is valid after being authenticated.
    """


_RequiredClientCreateGraphqlApiuserPoolConfigTypeDef = TypedDict(
    "_RequiredClientCreateGraphqlApiuserPoolConfigTypeDef",
    {"userPoolId": str, "awsRegion": str, "defaultAction": str},
)
_OptionalClientCreateGraphqlApiuserPoolConfigTypeDef = TypedDict(
    "_OptionalClientCreateGraphqlApiuserPoolConfigTypeDef", {"appIdClientRegex": str}, total=False
)


class ClientCreateGraphqlApiuserPoolConfigTypeDef(
    _RequiredClientCreateGraphqlApiuserPoolConfigTypeDef,
    _OptionalClientCreateGraphqlApiuserPoolConfigTypeDef,
):
    """
    Type definition for `ClientCreateGraphqlApi` `userPoolConfig`

    The Amazon Cognito user pool configuration.

    - **userPoolId** *(string) --* **[REQUIRED]**

      The user pool ID.

    - **awsRegion** *(string) --* **[REQUIRED]**

      The AWS Region in which the user pool was created.

    - **defaultAction** *(string) --* **[REQUIRED]**

      The action that you want your GraphQL API to take when a request that uses Amazon Cognito user
      pool authentication doesn't match the Amazon Cognito user pool configuration.

    - **appIdClientRegex** *(string) --*

      A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientCreateResolverResponseresolvercachingConfigTypeDef = TypedDict(
    "_ClientCreateResolverResponseresolvercachingConfigTypeDef",
    {"ttl": int, "cachingKeys": List[str]},
    total=False,
)


class ClientCreateResolverResponseresolvercachingConfigTypeDef(
    _ClientCreateResolverResponseresolvercachingConfigTypeDef
):
    """
    Type definition for `ClientCreateResolverResponseresolver` `cachingConfig`

    The caching configuration for the resolver.

    - **ttl** *(integer) --*

      The TTL in seconds for a resolver that has caching enabled.

      Valid values are between 1 and 3600 seconds.

    - **cachingKeys** *(list) --*

      The caching keys for a resolver that has caching enabled.

      Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

      - *(string) --*
    """


_ClientCreateResolverResponseresolverpipelineConfigTypeDef = TypedDict(
    "_ClientCreateResolverResponseresolverpipelineConfigTypeDef",
    {"functions": List[str]},
    total=False,
)


class ClientCreateResolverResponseresolverpipelineConfigTypeDef(
    _ClientCreateResolverResponseresolverpipelineConfigTypeDef
):
    """
    Type definition for `ClientCreateResolverResponseresolver` `pipelineConfig`

    The ``PipelineConfig`` .

    - **functions** *(list) --*

      A list of ``Function`` objects.

      - *(string) --*
    """


_ClientCreateResolverResponseresolversyncConfiglambdaConflictHandlerConfigTypeDef = TypedDict(
    "_ClientCreateResolverResponseresolversyncConfiglambdaConflictHandlerConfigTypeDef",
    {"lambdaConflictHandlerArn": str},
    total=False,
)


class ClientCreateResolverResponseresolversyncConfiglambdaConflictHandlerConfigTypeDef(
    _ClientCreateResolverResponseresolversyncConfiglambdaConflictHandlerConfigTypeDef
):
    """
    Type definition for `ClientCreateResolverResponseresolversyncConfig`
    `lambdaConflictHandlerConfig`

    The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

    - **lambdaConflictHandlerArn** *(string) --*

      The Arn for the Lambda function to use as the Conflict Handler.
    """


_ClientCreateResolverResponseresolversyncConfigTypeDef = TypedDict(
    "_ClientCreateResolverResponseresolversyncConfigTypeDef",
    {
        "conflictHandler": str,
        "conflictDetection": str,
        "lambdaConflictHandlerConfig": ClientCreateResolverResponseresolversyncConfiglambdaConflictHandlerConfigTypeDef,
    },
    total=False,
)


class ClientCreateResolverResponseresolversyncConfigTypeDef(
    _ClientCreateResolverResponseresolversyncConfigTypeDef
):
    """
    Type definition for `ClientCreateResolverResponseresolver` `syncConfig`

    The ``SyncConfig`` for a resolver attached to a versioned datasource.

    - **conflictHandler** *(string) --*

      The Conflict Resolution strategy to perform in the event of a conflict.

      * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do not
      match the latest version at the server.

      * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

      * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
      LambdaConflictHandlerConfig.

    - **conflictDetection** *(string) --*

      The Conflict Detection strategy to use.

      * **VERSION** : Detect conflicts based on object versions for this resolver.

      * **NONE** : Do not detect conflicts when executing this resolver.

    - **lambdaConflictHandlerConfig** *(dict) --*

      The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

      - **lambdaConflictHandlerArn** *(string) --*

        The Arn for the Lambda function to use as the Conflict Handler.
    """


_ClientCreateResolverResponseresolverTypeDef = TypedDict(
    "_ClientCreateResolverResponseresolverTypeDef",
    {
        "typeName": str,
        "fieldName": str,
        "dataSourceName": str,
        "resolverArn": str,
        "requestMappingTemplate": str,
        "responseMappingTemplate": str,
        "kind": str,
        "pipelineConfig": ClientCreateResolverResponseresolverpipelineConfigTypeDef,
        "syncConfig": ClientCreateResolverResponseresolversyncConfigTypeDef,
        "cachingConfig": ClientCreateResolverResponseresolvercachingConfigTypeDef,
    },
    total=False,
)


class ClientCreateResolverResponseresolverTypeDef(_ClientCreateResolverResponseresolverTypeDef):
    """
    Type definition for `ClientCreateResolverResponse` `resolver`

    The ``Resolver`` object.

    - **typeName** *(string) --*

      The resolver type name.

    - **fieldName** *(string) --*

      The resolver field name.

    - **dataSourceName** *(string) --*

      The resolver data source name.

    - **resolverArn** *(string) --*

      The resolver ARN.

    - **requestMappingTemplate** *(string) --*

      The request mapping template.

    - **responseMappingTemplate** *(string) --*

      The response mapping template.

    - **kind** *(string) --*

      The resolver type.

      * **UNIT** : A UNIT resolver type. A UNIT resolver is the default resolver type. A UNIT
      resolver enables you to execute a GraphQL query against a single data source.

      * **PIPELINE** : A PIPELINE resolver type. A PIPELINE resolver enables you to execute a series
      of ``Function`` in a serial manner. You can use a pipeline resolver to execute a GraphQL query
      against multiple data sources.

    - **pipelineConfig** *(dict) --*

      The ``PipelineConfig`` .

      - **functions** *(list) --*

        A list of ``Function`` objects.

        - *(string) --*

    - **syncConfig** *(dict) --*

      The ``SyncConfig`` for a resolver attached to a versioned datasource.

      - **conflictHandler** *(string) --*

        The Conflict Resolution strategy to perform in the event of a conflict.

        * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do not
        match the latest version at the server.

        * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

        * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
        LambdaConflictHandlerConfig.

      - **conflictDetection** *(string) --*

        The Conflict Detection strategy to use.

        * **VERSION** : Detect conflicts based on object versions for this resolver.

        * **NONE** : Do not detect conflicts when executing this resolver.

      - **lambdaConflictHandlerConfig** *(dict) --*

        The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

        - **lambdaConflictHandlerArn** *(string) --*

          The Arn for the Lambda function to use as the Conflict Handler.

    - **cachingConfig** *(dict) --*

      The caching configuration for the resolver.

      - **ttl** *(integer) --*

        The TTL in seconds for a resolver that has caching enabled.

        Valid values are between 1 and 3600 seconds.

      - **cachingKeys** *(list) --*

        The caching keys for a resolver that has caching enabled.

        Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

        - *(string) --*
    """


_ClientCreateResolverResponseTypeDef = TypedDict(
    "_ClientCreateResolverResponseTypeDef",
    {"resolver": ClientCreateResolverResponseresolverTypeDef},
    total=False,
)


class ClientCreateResolverResponseTypeDef(_ClientCreateResolverResponseTypeDef):
    """
    Type definition for `ClientCreateResolver` `Response`

    - **resolver** *(dict) --*

      The ``Resolver`` object.

      - **typeName** *(string) --*

        The resolver type name.

      - **fieldName** *(string) --*

        The resolver field name.

      - **dataSourceName** *(string) --*

        The resolver data source name.

      - **resolverArn** *(string) --*

        The resolver ARN.

      - **requestMappingTemplate** *(string) --*

        The request mapping template.

      - **responseMappingTemplate** *(string) --*

        The response mapping template.

      - **kind** *(string) --*

        The resolver type.

        * **UNIT** : A UNIT resolver type. A UNIT resolver is the default resolver type. A UNIT
        resolver enables you to execute a GraphQL query against a single data source.

        * **PIPELINE** : A PIPELINE resolver type. A PIPELINE resolver enables you to execute a
        series of ``Function`` in a serial manner. You can use a pipeline resolver to execute a
        GraphQL query against multiple data sources.

      - **pipelineConfig** *(dict) --*

        The ``PipelineConfig`` .

        - **functions** *(list) --*

          A list of ``Function`` objects.

          - *(string) --*

      - **syncConfig** *(dict) --*

        The ``SyncConfig`` for a resolver attached to a versioned datasource.

        - **conflictHandler** *(string) --*

          The Conflict Resolution strategy to perform in the event of a conflict.

          * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do
          not match the latest version at the server.

          * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

          * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
          LambdaConflictHandlerConfig.

        - **conflictDetection** *(string) --*

          The Conflict Detection strategy to use.

          * **VERSION** : Detect conflicts based on object versions for this resolver.

          * **NONE** : Do not detect conflicts when executing this resolver.

        - **lambdaConflictHandlerConfig** *(dict) --*

          The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

          - **lambdaConflictHandlerArn** *(string) --*

            The Arn for the Lambda function to use as the Conflict Handler.

      - **cachingConfig** *(dict) --*

        The caching configuration for the resolver.

        - **ttl** *(integer) --*

          The TTL in seconds for a resolver that has caching enabled.

          Valid values are between 1 and 3600 seconds.

        - **cachingKeys** *(list) --*

          The caching keys for a resolver that has caching enabled.

          Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

          - *(string) --*
    """


_ClientCreateResolvercachingConfigTypeDef = TypedDict(
    "_ClientCreateResolvercachingConfigTypeDef", {"ttl": int, "cachingKeys": List[str]}, total=False
)


class ClientCreateResolvercachingConfigTypeDef(_ClientCreateResolvercachingConfigTypeDef):
    """
    Type definition for `ClientCreateResolver` `cachingConfig`

    The caching configuration for the resolver.

    - **ttl** *(integer) --*

      The TTL in seconds for a resolver that has caching enabled.

      Valid values are between 1 and 3600 seconds.

    - **cachingKeys** *(list) --*

      The caching keys for a resolver that has caching enabled.

      Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

      - *(string) --*
    """


_ClientCreateResolverpipelineConfigTypeDef = TypedDict(
    "_ClientCreateResolverpipelineConfigTypeDef", {"functions": List[str]}, total=False
)


class ClientCreateResolverpipelineConfigTypeDef(_ClientCreateResolverpipelineConfigTypeDef):
    """
    Type definition for `ClientCreateResolver` `pipelineConfig`

    The ``PipelineConfig`` .

    - **functions** *(list) --*

      A list of ``Function`` objects.

      - *(string) --*
    """


_ClientCreateResolversyncConfiglambdaConflictHandlerConfigTypeDef = TypedDict(
    "_ClientCreateResolversyncConfiglambdaConflictHandlerConfigTypeDef",
    {"lambdaConflictHandlerArn": str},
    total=False,
)


class ClientCreateResolversyncConfiglambdaConflictHandlerConfigTypeDef(
    _ClientCreateResolversyncConfiglambdaConflictHandlerConfigTypeDef
):
    """
    Type definition for `ClientCreateResolversyncConfig` `lambdaConflictHandlerConfig`

    The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

    - **lambdaConflictHandlerArn** *(string) --*

      The Arn for the Lambda function to use as the Conflict Handler.
    """


_ClientCreateResolversyncConfigTypeDef = TypedDict(
    "_ClientCreateResolversyncConfigTypeDef",
    {
        "conflictHandler": str,
        "conflictDetection": str,
        "lambdaConflictHandlerConfig": ClientCreateResolversyncConfiglambdaConflictHandlerConfigTypeDef,
    },
    total=False,
)


class ClientCreateResolversyncConfigTypeDef(_ClientCreateResolversyncConfigTypeDef):
    """
    Type definition for `ClientCreateResolver` `syncConfig`

    The ``SyncConfig`` for a resolver attached to a versioned datasource.

    - **conflictHandler** *(string) --*

      The Conflict Resolution strategy to perform in the event of a conflict.

      * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do not
      match the latest version at the server.

      * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

      * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
      LambdaConflictHandlerConfig.

    - **conflictDetection** *(string) --*

      The Conflict Detection strategy to use.

      * **VERSION** : Detect conflicts based on object versions for this resolver.

      * **NONE** : Do not detect conflicts when executing this resolver.

    - **lambdaConflictHandlerConfig** *(dict) --*

      The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

      - **lambdaConflictHandlerArn** *(string) --*

        The Arn for the Lambda function to use as the Conflict Handler.
    """


_ClientCreateTypeResponsetypeTypeDef = TypedDict(
    "_ClientCreateTypeResponsetypeTypeDef",
    {"name": str, "description": str, "arn": str, "definition": str, "format": str},
    total=False,
)


class ClientCreateTypeResponsetypeTypeDef(_ClientCreateTypeResponsetypeTypeDef):
    """
    Type definition for `ClientCreateTypeResponse` `type`

    The ``Type`` object.

    - **name** *(string) --*

      The type name.

    - **description** *(string) --*

      The type description.

    - **arn** *(string) --*

      The type ARN.

    - **definition** *(string) --*

      The type definition.

    - **format** *(string) --*

      The type format: SDL or JSON.
    """


_ClientCreateTypeResponseTypeDef = TypedDict(
    "_ClientCreateTypeResponseTypeDef", {"type": ClientCreateTypeResponsetypeTypeDef}, total=False
)


class ClientCreateTypeResponseTypeDef(_ClientCreateTypeResponseTypeDef):
    """
    Type definition for `ClientCreateType` `Response`

    - **type** *(dict) --*

      The ``Type`` object.

      - **name** *(string) --*

        The type name.

      - **description** *(string) --*

        The type description.

      - **arn** *(string) --*

        The type ARN.

      - **definition** *(string) --*

        The type definition.

      - **format** *(string) --*

        The type format: SDL or JSON.
    """


_ClientGetApiCacheResponseapiCacheTypeDef = TypedDict(
    "_ClientGetApiCacheResponseapiCacheTypeDef",
    {
        "ttl": int,
        "apiCachingBehavior": str,
        "transitEncryptionEnabled": bool,
        "atRestEncryptionEnabled": bool,
        "type": str,
        "status": str,
    },
    total=False,
)


class ClientGetApiCacheResponseapiCacheTypeDef(_ClientGetApiCacheResponseapiCacheTypeDef):
    """
    Type definition for `ClientGetApiCacheResponse` `apiCache`

    - **ttl** *(integer) --*

      TTL in seconds for cache entries.

      Valid values are between 1 and 3600 seconds.

    - **apiCachingBehavior** *(string) --*

      Caching behavior.

      * **FULL_REQUEST_CACHING** : All requests are fully cached.

      * **PER_RESOLVER_CACHING** : Individual resovlers that you specify are cached.

    - **transitEncryptionEnabled** *(boolean) --*

      Transit encryption flag when connecting to cache. This setting cannot be updated after
      creation.

    - **atRestEncryptionEnabled** *(boolean) --*

      At rest encryption flag for cache. This setting cannot be updated after creation.

    - **type** *(string) --*

      The cache instance type.

      * **T2_SMALL** : A t2.small instance type.

      * **T2_MEDIUM** : A t2.medium instance type.

      * **R4_LARGE** : A r4.large instance type.

      * **R4_XLARGE** : A r4.xlarge instance type.

      * **R4_2XLARGE** : A r4.2xlarge instance type.

      * **R4_4XLARGE** : A r4.4xlarge instance type.

      * **R4_8XLARGE** : A r4.8xlarge instance type.

    - **status** *(string) --*

      The cache instance status.

      * **AVAILABLE** : The instance is available for use.

      * **CREATING** : The instance is currently creating.

      * **DELETING** : The instance is currently deleting.

      * **MODIFYING** : The instance is currently modifying.

      * **FAILED** : The instance has failed creation.
    """


_ClientGetApiCacheResponseTypeDef = TypedDict(
    "_ClientGetApiCacheResponseTypeDef",
    {"apiCache": ClientGetApiCacheResponseapiCacheTypeDef},
    total=False,
)


class ClientGetApiCacheResponseTypeDef(_ClientGetApiCacheResponseTypeDef):
    """
    Type definition for `ClientGetApiCache` `Response`

    Represents the output of a ``GetApiCache`` operation.

    - **apiCache** *(dict) --*

      - **ttl** *(integer) --*

        TTL in seconds for cache entries.

        Valid values are between 1 and 3600 seconds.

      - **apiCachingBehavior** *(string) --*

        Caching behavior.

        * **FULL_REQUEST_CACHING** : All requests are fully cached.

        * **PER_RESOLVER_CACHING** : Individual resovlers that you specify are cached.

      - **transitEncryptionEnabled** *(boolean) --*

        Transit encryption flag when connecting to cache. This setting cannot be updated after
        creation.

      - **atRestEncryptionEnabled** *(boolean) --*

        At rest encryption flag for cache. This setting cannot be updated after creation.

      - **type** *(string) --*

        The cache instance type.

        * **T2_SMALL** : A t2.small instance type.

        * **T2_MEDIUM** : A t2.medium instance type.

        * **R4_LARGE** : A r4.large instance type.

        * **R4_XLARGE** : A r4.xlarge instance type.

        * **R4_2XLARGE** : A r4.2xlarge instance type.

        * **R4_4XLARGE** : A r4.4xlarge instance type.

        * **R4_8XLARGE** : A r4.8xlarge instance type.

      - **status** *(string) --*

        The cache instance status.

        * **AVAILABLE** : The instance is available for use.

        * **CREATING** : The instance is currently creating.

        * **DELETING** : The instance is currently deleting.

        * **MODIFYING** : The instance is currently modifying.

        * **FAILED** : The instance has failed creation.
    """


_ClientGetDataSourceResponsedataSourcedynamodbConfigdeltaSyncConfigTypeDef = TypedDict(
    "_ClientGetDataSourceResponsedataSourcedynamodbConfigdeltaSyncConfigTypeDef",
    {"baseTableTTL": int, "deltaSyncTableName": str, "deltaSyncTableTTL": int},
    total=False,
)


class ClientGetDataSourceResponsedataSourcedynamodbConfigdeltaSyncConfigTypeDef(
    _ClientGetDataSourceResponsedataSourcedynamodbConfigdeltaSyncConfigTypeDef
):
    """
    Type definition for `ClientGetDataSourceResponsedataSourcedynamodbConfig` `deltaSyncConfig`

    The ``DeltaSyncConfig`` for a versioned datasource.

    - **baseTableTTL** *(integer) --*

      The number of minutes an Item is stored in the datasource.

    - **deltaSyncTableName** *(string) --*

      The Delta Sync table name.

    - **deltaSyncTableTTL** *(integer) --*

      The number of minutes a Delta Sync log entry is stored in the Delta Sync table.
    """


_ClientGetDataSourceResponsedataSourcedynamodbConfigTypeDef = TypedDict(
    "_ClientGetDataSourceResponsedataSourcedynamodbConfigTypeDef",
    {
        "tableName": str,
        "awsRegion": str,
        "useCallerCredentials": bool,
        "deltaSyncConfig": ClientGetDataSourceResponsedataSourcedynamodbConfigdeltaSyncConfigTypeDef,
        "versioned": bool,
    },
    total=False,
)


class ClientGetDataSourceResponsedataSourcedynamodbConfigTypeDef(
    _ClientGetDataSourceResponsedataSourcedynamodbConfigTypeDef
):
    """
    Type definition for `ClientGetDataSourceResponsedataSource` `dynamodbConfig`

    Amazon DynamoDB settings.

    - **tableName** *(string) --*

      The table name.

    - **awsRegion** *(string) --*

      The AWS Region.

    - **useCallerCredentials** *(boolean) --*

      Set to TRUE to use Amazon Cognito credentials with this data source.

    - **deltaSyncConfig** *(dict) --*

      The ``DeltaSyncConfig`` for a versioned datasource.

      - **baseTableTTL** *(integer) --*

        The number of minutes an Item is stored in the datasource.

      - **deltaSyncTableName** *(string) --*

        The Delta Sync table name.

      - **deltaSyncTableTTL** *(integer) --*

        The number of minutes a Delta Sync log entry is stored in the Delta Sync table.

    - **versioned** *(boolean) --*

      Set to TRUE to use Conflict Detection and Resolution with this data source.
    """


_ClientGetDataSourceResponsedataSourceelasticsearchConfigTypeDef = TypedDict(
    "_ClientGetDataSourceResponsedataSourceelasticsearchConfigTypeDef",
    {"endpoint": str, "awsRegion": str},
    total=False,
)


class ClientGetDataSourceResponsedataSourceelasticsearchConfigTypeDef(
    _ClientGetDataSourceResponsedataSourceelasticsearchConfigTypeDef
):
    """
    Type definition for `ClientGetDataSourceResponsedataSource` `elasticsearchConfig`

    Amazon Elasticsearch Service settings.

    - **endpoint** *(string) --*

      The endpoint.

    - **awsRegion** *(string) --*

      The AWS Region.
    """


_ClientGetDataSourceResponsedataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef = TypedDict(
    "_ClientGetDataSourceResponsedataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef",
    {"signingRegion": str, "signingServiceName": str},
    total=False,
)


class ClientGetDataSourceResponsedataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef(
    _ClientGetDataSourceResponsedataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef
):
    """
    Type definition for `ClientGetDataSourceResponsedataSourcehttpConfigauthorizationConfig`
    `awsIamConfig`

    The AWS IAM settings.

    - **signingRegion** *(string) --*

      The signing region for AWS IAM authorization.

    - **signingServiceName** *(string) --*

      The signing service name for AWS IAM authorization.
    """


_ClientGetDataSourceResponsedataSourcehttpConfigauthorizationConfigTypeDef = TypedDict(
    "_ClientGetDataSourceResponsedataSourcehttpConfigauthorizationConfigTypeDef",
    {
        "authorizationType": str,
        "awsIamConfig": ClientGetDataSourceResponsedataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef,
    },
    total=False,
)


class ClientGetDataSourceResponsedataSourcehttpConfigauthorizationConfigTypeDef(
    _ClientGetDataSourceResponsedataSourcehttpConfigauthorizationConfigTypeDef
):
    """
    Type definition for `ClientGetDataSourceResponsedataSourcehttpConfig` `authorizationConfig`

    The authorization config in case the HTTP endpoint requires authorization.

    - **authorizationType** *(string) --*

      The authorization type required by the HTTP endpoint.

      * **AWS_IAM** : The authorization type is Sigv4.

    - **awsIamConfig** *(dict) --*

      The AWS IAM settings.

      - **signingRegion** *(string) --*

        The signing region for AWS IAM authorization.

      - **signingServiceName** *(string) --*

        The signing service name for AWS IAM authorization.
    """


_ClientGetDataSourceResponsedataSourcehttpConfigTypeDef = TypedDict(
    "_ClientGetDataSourceResponsedataSourcehttpConfigTypeDef",
    {
        "endpoint": str,
        "authorizationConfig": ClientGetDataSourceResponsedataSourcehttpConfigauthorizationConfigTypeDef,
    },
    total=False,
)


class ClientGetDataSourceResponsedataSourcehttpConfigTypeDef(
    _ClientGetDataSourceResponsedataSourcehttpConfigTypeDef
):
    """
    Type definition for `ClientGetDataSourceResponsedataSource` `httpConfig`

    HTTP endpoint settings.

    - **endpoint** *(string) --*

      The HTTP URL endpoint. You can either specify the domain name or IP, and port combination, and
      the URL scheme must be HTTP or HTTPS. If the port is not specified, AWS AppSync uses the
      default port 80 for the HTTP endpoint and port 443 for HTTPS endpoints.

    - **authorizationConfig** *(dict) --*

      The authorization config in case the HTTP endpoint requires authorization.

      - **authorizationType** *(string) --*

        The authorization type required by the HTTP endpoint.

        * **AWS_IAM** : The authorization type is Sigv4.

      - **awsIamConfig** *(dict) --*

        The AWS IAM settings.

        - **signingRegion** *(string) --*

          The signing region for AWS IAM authorization.

        - **signingServiceName** *(string) --*

          The signing service name for AWS IAM authorization.
    """


_ClientGetDataSourceResponsedataSourcelambdaConfigTypeDef = TypedDict(
    "_ClientGetDataSourceResponsedataSourcelambdaConfigTypeDef",
    {"lambdaFunctionArn": str},
    total=False,
)


class ClientGetDataSourceResponsedataSourcelambdaConfigTypeDef(
    _ClientGetDataSourceResponsedataSourcelambdaConfigTypeDef
):
    """
    Type definition for `ClientGetDataSourceResponsedataSource` `lambdaConfig`

    AWS Lambda settings.

    - **lambdaFunctionArn** *(string) --*

      The ARN for the Lambda function.
    """


_ClientGetDataSourceResponsedataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef = TypedDict(
    "_ClientGetDataSourceResponsedataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef",
    {
        "awsRegion": str,
        "dbClusterIdentifier": str,
        "databaseName": str,
        "schema": str,
        "awsSecretStoreArn": str,
    },
    total=False,
)


class ClientGetDataSourceResponsedataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef(
    _ClientGetDataSourceResponsedataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef
):
    """
    Type definition for `ClientGetDataSourceResponsedataSourcerelationalDatabaseConfig`
    `rdsHttpEndpointConfig`

    Amazon RDS HTTP endpoint settings.

    - **awsRegion** *(string) --*

      AWS Region for RDS HTTP endpoint.

    - **dbClusterIdentifier** *(string) --*

      Amazon RDS cluster identifier.

    - **databaseName** *(string) --*

      Logical database name.

    - **schema** *(string) --*

      Logical schema name.

    - **awsSecretStoreArn** *(string) --*

      AWS secret store ARN for database credentials.
    """


_ClientGetDataSourceResponsedataSourcerelationalDatabaseConfigTypeDef = TypedDict(
    "_ClientGetDataSourceResponsedataSourcerelationalDatabaseConfigTypeDef",
    {
        "relationalDatabaseSourceType": str,
        "rdsHttpEndpointConfig": ClientGetDataSourceResponsedataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef,
    },
    total=False,
)


class ClientGetDataSourceResponsedataSourcerelationalDatabaseConfigTypeDef(
    _ClientGetDataSourceResponsedataSourcerelationalDatabaseConfigTypeDef
):
    """
    Type definition for `ClientGetDataSourceResponsedataSource` `relationalDatabaseConfig`

    Relational database settings.

    - **relationalDatabaseSourceType** *(string) --*

      Source type for the relational database.

      * **RDS_HTTP_ENDPOINT** : The relational database source type is an Amazon RDS HTTP endpoint.

    - **rdsHttpEndpointConfig** *(dict) --*

      Amazon RDS HTTP endpoint settings.

      - **awsRegion** *(string) --*

        AWS Region for RDS HTTP endpoint.

      - **dbClusterIdentifier** *(string) --*

        Amazon RDS cluster identifier.

      - **databaseName** *(string) --*

        Logical database name.

      - **schema** *(string) --*

        Logical schema name.

      - **awsSecretStoreArn** *(string) --*

        AWS secret store ARN for database credentials.
    """


_ClientGetDataSourceResponsedataSourceTypeDef = TypedDict(
    "_ClientGetDataSourceResponsedataSourceTypeDef",
    {
        "dataSourceArn": str,
        "name": str,
        "description": str,
        "type": str,
        "serviceRoleArn": str,
        "dynamodbConfig": ClientGetDataSourceResponsedataSourcedynamodbConfigTypeDef,
        "lambdaConfig": ClientGetDataSourceResponsedataSourcelambdaConfigTypeDef,
        "elasticsearchConfig": ClientGetDataSourceResponsedataSourceelasticsearchConfigTypeDef,
        "httpConfig": ClientGetDataSourceResponsedataSourcehttpConfigTypeDef,
        "relationalDatabaseConfig": ClientGetDataSourceResponsedataSourcerelationalDatabaseConfigTypeDef,
    },
    total=False,
)


class ClientGetDataSourceResponsedataSourceTypeDef(_ClientGetDataSourceResponsedataSourceTypeDef):
    """
    Type definition for `ClientGetDataSourceResponse` `dataSource`

    The ``DataSource`` object.

    - **dataSourceArn** *(string) --*

      The data source ARN.

    - **name** *(string) --*

      The name of the data source.

    - **description** *(string) --*

      The description of the data source.

    - **type** *(string) --*

      The type of the data source.

      * **AMAZON_DYNAMODB** : The data source is an Amazon DynamoDB table.

      * **AMAZON_ELASTICSEARCH** : The data source is an Amazon Elasticsearch Service domain.

      * **AWS_LAMBDA** : The data source is an AWS Lambda function.

      * **NONE** : There is no data source. This type is used when you wish to invoke a GraphQL
      operation without connecting to a data source, such as performing data transformation with
      resolvers or triggering a subscription to be invoked from a mutation.

      * **HTTP** : The data source is an HTTP endpoint.

      * **RELATIONAL_DATABASE** : The data source is a relational database.

    - **serviceRoleArn** *(string) --*

      The AWS IAM service role ARN for the data source. The system assumes this role when accessing
      the data source.

    - **dynamodbConfig** *(dict) --*

      Amazon DynamoDB settings.

      - **tableName** *(string) --*

        The table name.

      - **awsRegion** *(string) --*

        The AWS Region.

      - **useCallerCredentials** *(boolean) --*

        Set to TRUE to use Amazon Cognito credentials with this data source.

      - **deltaSyncConfig** *(dict) --*

        The ``DeltaSyncConfig`` for a versioned datasource.

        - **baseTableTTL** *(integer) --*

          The number of minutes an Item is stored in the datasource.

        - **deltaSyncTableName** *(string) --*

          The Delta Sync table name.

        - **deltaSyncTableTTL** *(integer) --*

          The number of minutes a Delta Sync log entry is stored in the Delta Sync table.

      - **versioned** *(boolean) --*

        Set to TRUE to use Conflict Detection and Resolution with this data source.

    - **lambdaConfig** *(dict) --*

      AWS Lambda settings.

      - **lambdaFunctionArn** *(string) --*

        The ARN for the Lambda function.

    - **elasticsearchConfig** *(dict) --*

      Amazon Elasticsearch Service settings.

      - **endpoint** *(string) --*

        The endpoint.

      - **awsRegion** *(string) --*

        The AWS Region.

    - **httpConfig** *(dict) --*

      HTTP endpoint settings.

      - **endpoint** *(string) --*

        The HTTP URL endpoint. You can either specify the domain name or IP, and port combination,
        and the URL scheme must be HTTP or HTTPS. If the port is not specified, AWS AppSync uses the
        default port 80 for the HTTP endpoint and port 443 for HTTPS endpoints.

      - **authorizationConfig** *(dict) --*

        The authorization config in case the HTTP endpoint requires authorization.

        - **authorizationType** *(string) --*

          The authorization type required by the HTTP endpoint.

          * **AWS_IAM** : The authorization type is Sigv4.

        - **awsIamConfig** *(dict) --*

          The AWS IAM settings.

          - **signingRegion** *(string) --*

            The signing region for AWS IAM authorization.

          - **signingServiceName** *(string) --*

            The signing service name for AWS IAM authorization.

    - **relationalDatabaseConfig** *(dict) --*

      Relational database settings.

      - **relationalDatabaseSourceType** *(string) --*

        Source type for the relational database.

        * **RDS_HTTP_ENDPOINT** : The relational database source type is an Amazon RDS HTTP
        endpoint.

      - **rdsHttpEndpointConfig** *(dict) --*

        Amazon RDS HTTP endpoint settings.

        - **awsRegion** *(string) --*

          AWS Region for RDS HTTP endpoint.

        - **dbClusterIdentifier** *(string) --*

          Amazon RDS cluster identifier.

        - **databaseName** *(string) --*

          Logical database name.

        - **schema** *(string) --*

          Logical schema name.

        - **awsSecretStoreArn** *(string) --*

          AWS secret store ARN for database credentials.
    """


_ClientGetDataSourceResponseTypeDef = TypedDict(
    "_ClientGetDataSourceResponseTypeDef",
    {"dataSource": ClientGetDataSourceResponsedataSourceTypeDef},
    total=False,
)


class ClientGetDataSourceResponseTypeDef(_ClientGetDataSourceResponseTypeDef):
    """
    Type definition for `ClientGetDataSource` `Response`

    - **dataSource** *(dict) --*

      The ``DataSource`` object.

      - **dataSourceArn** *(string) --*

        The data source ARN.

      - **name** *(string) --*

        The name of the data source.

      - **description** *(string) --*

        The description of the data source.

      - **type** *(string) --*

        The type of the data source.

        * **AMAZON_DYNAMODB** : The data source is an Amazon DynamoDB table.

        * **AMAZON_ELASTICSEARCH** : The data source is an Amazon Elasticsearch Service domain.

        * **AWS_LAMBDA** : The data source is an AWS Lambda function.

        * **NONE** : There is no data source. This type is used when you wish to invoke a GraphQL
        operation without connecting to a data source, such as performing data transformation with
        resolvers or triggering a subscription to be invoked from a mutation.

        * **HTTP** : The data source is an HTTP endpoint.

        * **RELATIONAL_DATABASE** : The data source is a relational database.

      - **serviceRoleArn** *(string) --*

        The AWS IAM service role ARN for the data source. The system assumes this role when
        accessing the data source.

      - **dynamodbConfig** *(dict) --*

        Amazon DynamoDB settings.

        - **tableName** *(string) --*

          The table name.

        - **awsRegion** *(string) --*

          The AWS Region.

        - **useCallerCredentials** *(boolean) --*

          Set to TRUE to use Amazon Cognito credentials with this data source.

        - **deltaSyncConfig** *(dict) --*

          The ``DeltaSyncConfig`` for a versioned datasource.

          - **baseTableTTL** *(integer) --*

            The number of minutes an Item is stored in the datasource.

          - **deltaSyncTableName** *(string) --*

            The Delta Sync table name.

          - **deltaSyncTableTTL** *(integer) --*

            The number of minutes a Delta Sync log entry is stored in the Delta Sync table.

        - **versioned** *(boolean) --*

          Set to TRUE to use Conflict Detection and Resolution with this data source.

      - **lambdaConfig** *(dict) --*

        AWS Lambda settings.

        - **lambdaFunctionArn** *(string) --*

          The ARN for the Lambda function.

      - **elasticsearchConfig** *(dict) --*

        Amazon Elasticsearch Service settings.

        - **endpoint** *(string) --*

          The endpoint.

        - **awsRegion** *(string) --*

          The AWS Region.

      - **httpConfig** *(dict) --*

        HTTP endpoint settings.

        - **endpoint** *(string) --*

          The HTTP URL endpoint. You can either specify the domain name or IP, and port combination,
          and the URL scheme must be HTTP or HTTPS. If the port is not specified, AWS AppSync uses
          the default port 80 for the HTTP endpoint and port 443 for HTTPS endpoints.

        - **authorizationConfig** *(dict) --*

          The authorization config in case the HTTP endpoint requires authorization.

          - **authorizationType** *(string) --*

            The authorization type required by the HTTP endpoint.

            * **AWS_IAM** : The authorization type is Sigv4.

          - **awsIamConfig** *(dict) --*

            The AWS IAM settings.

            - **signingRegion** *(string) --*

              The signing region for AWS IAM authorization.

            - **signingServiceName** *(string) --*

              The signing service name for AWS IAM authorization.

      - **relationalDatabaseConfig** *(dict) --*

        Relational database settings.

        - **relationalDatabaseSourceType** *(string) --*

          Source type for the relational database.

          * **RDS_HTTP_ENDPOINT** : The relational database source type is an Amazon RDS HTTP
          endpoint.

        - **rdsHttpEndpointConfig** *(dict) --*

          Amazon RDS HTTP endpoint settings.

          - **awsRegion** *(string) --*

            AWS Region for RDS HTTP endpoint.

          - **dbClusterIdentifier** *(string) --*

            Amazon RDS cluster identifier.

          - **databaseName** *(string) --*

            Logical database name.

          - **schema** *(string) --*

            Logical schema name.

          - **awsSecretStoreArn** *(string) --*

            AWS secret store ARN for database credentials.
    """


_ClientGetFunctionResponsefunctionConfigurationTypeDef = TypedDict(
    "_ClientGetFunctionResponsefunctionConfigurationTypeDef",
    {
        "functionId": str,
        "functionArn": str,
        "name": str,
        "description": str,
        "dataSourceName": str,
        "requestMappingTemplate": str,
        "responseMappingTemplate": str,
        "functionVersion": str,
    },
    total=False,
)


class ClientGetFunctionResponsefunctionConfigurationTypeDef(
    _ClientGetFunctionResponsefunctionConfigurationTypeDef
):
    """
    Type definition for `ClientGetFunctionResponse` `functionConfiguration`

    The ``Function`` object.

    - **functionId** *(string) --*

      A unique ID representing the ``Function`` object.

    - **functionArn** *(string) --*

      The ARN of the ``Function`` object.

    - **name** *(string) --*

      The name of the ``Function`` object.

    - **description** *(string) --*

      The ``Function`` description.

    - **dataSourceName** *(string) --*

      The name of the ``DataSource`` .

    - **requestMappingTemplate** *(string) --*

      The ``Function`` request mapping template. Functions support only the 2018-05-29 version of
      the request mapping template.

    - **responseMappingTemplate** *(string) --*

      The ``Function`` response mapping template.

    - **functionVersion** *(string) --*

      The version of the request mapping template. Currently only the 2018-05-29 version of the
      template is supported.
    """


_ClientGetFunctionResponseTypeDef = TypedDict(
    "_ClientGetFunctionResponseTypeDef",
    {"functionConfiguration": ClientGetFunctionResponsefunctionConfigurationTypeDef},
    total=False,
)


class ClientGetFunctionResponseTypeDef(_ClientGetFunctionResponseTypeDef):
    """
    Type definition for `ClientGetFunction` `Response`

    - **functionConfiguration** *(dict) --*

      The ``Function`` object.

      - **functionId** *(string) --*

        A unique ID representing the ``Function`` object.

      - **functionArn** *(string) --*

        The ARN of the ``Function`` object.

      - **name** *(string) --*

        The name of the ``Function`` object.

      - **description** *(string) --*

        The ``Function`` description.

      - **dataSourceName** *(string) --*

        The name of the ``DataSource`` .

      - **requestMappingTemplate** *(string) --*

        The ``Function`` request mapping template. Functions support only the 2018-05-29 version of
        the request mapping template.

      - **responseMappingTemplate** *(string) --*

        The ``Function`` response mapping template.

      - **functionVersion** *(string) --*

        The version of the request mapping template. Currently only the 2018-05-29 version of the
        template is supported.
    """


_ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef = TypedDict(
    "_ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef",
    {"issuer": str, "clientId": str, "iatTTL": int, "authTTL": int},
    total=False,
)


class ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef(
    _ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef
):
    """
    Type definition for `ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProviders`
    `openIDConnectConfig`

    The OpenID Connect configuration.

    - **issuer** *(string) --*

      The issuer for the OpenID Connect configuration. The issuer returned by discovery must exactly
      match the value of ``iss`` in the ID token.

    - **clientId** *(string) --*

      The client identifier of the Relying party at the OpenID identity provider. This identifier is
      typically obtained when the Relying party is registered with the OpenID identity provider. You
      can specify a regular expression so the AWS AppSync can validate against multiple client
      identifiers at a time.

    - **iatTTL** *(integer) --*

      The number of milliseconds a token is valid after being issued to a user.

    - **authTTL** *(integer) --*

      The number of milliseconds a token is valid after being authenticated.
    """


_ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef = TypedDict(
    "_ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef",
    {"userPoolId": str, "awsRegion": str, "appIdClientRegex": str},
    total=False,
)


class ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef(
    _ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef
):
    """
    Type definition for `ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProviders`
    `userPoolConfig`

    The Amazon Cognito user pool configuration.

    - **userPoolId** *(string) --*

      The user pool ID.

    - **awsRegion** *(string) --*

      The AWS Region in which the user pool was created.

    - **appIdClientRegex** *(string) --*

      A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersTypeDef = TypedDict(
    "_ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersTypeDef",
    {
        "authenticationType": str,
        "openIDConnectConfig": ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef,
        "userPoolConfig": ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef,
    },
    total=False,
)


class ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersTypeDef(
    _ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersTypeDef
):
    """
    Type definition for `ClientGetGraphqlApiResponsegraphqlApi` `additionalAuthenticationProviders`

    Describes an additional authentication provider.

    - **authenticationType** *(string) --*

      The authentication type: API key, AWS IAM, OIDC, or Amazon Cognito user pools.

    - **openIDConnectConfig** *(dict) --*

      The OpenID Connect configuration.

      - **issuer** *(string) --*

        The issuer for the OpenID Connect configuration. The issuer returned by discovery must
        exactly match the value of ``iss`` in the ID token.

      - **clientId** *(string) --*

        The client identifier of the Relying party at the OpenID identity provider. This identifier
        is typically obtained when the Relying party is registered with the OpenID identity
        provider. You can specify a regular expression so the AWS AppSync can validate against
        multiple client identifiers at a time.

      - **iatTTL** *(integer) --*

        The number of milliseconds a token is valid after being issued to a user.

      - **authTTL** *(integer) --*

        The number of milliseconds a token is valid after being authenticated.

    - **userPoolConfig** *(dict) --*

      The Amazon Cognito user pool configuration.

      - **userPoolId** *(string) --*

        The user pool ID.

      - **awsRegion** *(string) --*

        The AWS Region in which the user pool was created.

      - **appIdClientRegex** *(string) --*

        A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientGetGraphqlApiResponsegraphqlApilogConfigTypeDef = TypedDict(
    "_ClientGetGraphqlApiResponsegraphqlApilogConfigTypeDef",
    {"fieldLogLevel": str, "cloudWatchLogsRoleArn": str, "excludeVerboseContent": bool},
    total=False,
)


class ClientGetGraphqlApiResponsegraphqlApilogConfigTypeDef(
    _ClientGetGraphqlApiResponsegraphqlApilogConfigTypeDef
):
    """
    Type definition for `ClientGetGraphqlApiResponsegraphqlApi` `logConfig`

    The Amazon CloudWatch Logs configuration.

    - **fieldLogLevel** *(string) --*

      The field logging level. Values can be NONE, ERROR, or ALL.

      * **NONE** : No field-level logs are captured.

      * **ERROR** : Logs the following information only for the fields that are in error:

        * The error section in the server response.

        * Field-level errors.

        * The generated request/response functions that got resolved for error fields.

      * **ALL** : The following information is logged for all fields in the query:

        * Field-level tracing information.

        * The generated request/response functions that got resolved for each field.

    - **cloudWatchLogsRoleArn** *(string) --*

      The service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in your
      account.

    - **excludeVerboseContent** *(boolean) --*

      Set to TRUE to exclude sections that contain information such as headers, context, and
      evaluated mapping templates, regardless of logging level.
    """


_ClientGetGraphqlApiResponsegraphqlApiopenIDConnectConfigTypeDef = TypedDict(
    "_ClientGetGraphqlApiResponsegraphqlApiopenIDConnectConfigTypeDef",
    {"issuer": str, "clientId": str, "iatTTL": int, "authTTL": int},
    total=False,
)


class ClientGetGraphqlApiResponsegraphqlApiopenIDConnectConfigTypeDef(
    _ClientGetGraphqlApiResponsegraphqlApiopenIDConnectConfigTypeDef
):
    """
    Type definition for `ClientGetGraphqlApiResponsegraphqlApi` `openIDConnectConfig`

    The OpenID Connect configuration.

    - **issuer** *(string) --*

      The issuer for the OpenID Connect configuration. The issuer returned by discovery must exactly
      match the value of ``iss`` in the ID token.

    - **clientId** *(string) --*

      The client identifier of the Relying party at the OpenID identity provider. This identifier is
      typically obtained when the Relying party is registered with the OpenID identity provider. You
      can specify a regular expression so the AWS AppSync can validate against multiple client
      identifiers at a time.

    - **iatTTL** *(integer) --*

      The number of milliseconds a token is valid after being issued to a user.

    - **authTTL** *(integer) --*

      The number of milliseconds a token is valid after being authenticated.
    """


_ClientGetGraphqlApiResponsegraphqlApiuserPoolConfigTypeDef = TypedDict(
    "_ClientGetGraphqlApiResponsegraphqlApiuserPoolConfigTypeDef",
    {"userPoolId": str, "awsRegion": str, "defaultAction": str, "appIdClientRegex": str},
    total=False,
)


class ClientGetGraphqlApiResponsegraphqlApiuserPoolConfigTypeDef(
    _ClientGetGraphqlApiResponsegraphqlApiuserPoolConfigTypeDef
):
    """
    Type definition for `ClientGetGraphqlApiResponsegraphqlApi` `userPoolConfig`

    The Amazon Cognito user pool configuration.

    - **userPoolId** *(string) --*

      The user pool ID.

    - **awsRegion** *(string) --*

      The AWS Region in which the user pool was created.

    - **defaultAction** *(string) --*

      The action that you want your GraphQL API to take when a request that uses Amazon Cognito user
      pool authentication doesn't match the Amazon Cognito user pool configuration.

    - **appIdClientRegex** *(string) --*

      A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientGetGraphqlApiResponsegraphqlApiTypeDef = TypedDict(
    "_ClientGetGraphqlApiResponsegraphqlApiTypeDef",
    {
        "name": str,
        "apiId": str,
        "authenticationType": str,
        "logConfig": ClientGetGraphqlApiResponsegraphqlApilogConfigTypeDef,
        "userPoolConfig": ClientGetGraphqlApiResponsegraphqlApiuserPoolConfigTypeDef,
        "openIDConnectConfig": ClientGetGraphqlApiResponsegraphqlApiopenIDConnectConfigTypeDef,
        "arn": str,
        "uris": Dict[str, str],
        "tags": Dict[str, str],
        "additionalAuthenticationProviders": List[
            ClientGetGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersTypeDef
        ],
    },
    total=False,
)


class ClientGetGraphqlApiResponsegraphqlApiTypeDef(_ClientGetGraphqlApiResponsegraphqlApiTypeDef):
    """
    Type definition for `ClientGetGraphqlApiResponse` `graphqlApi`

    The ``GraphqlApi`` object.

    - **name** *(string) --*

      The API name.

    - **apiId** *(string) --*

      The API ID.

    - **authenticationType** *(string) --*

      The authentication type.

    - **logConfig** *(dict) --*

      The Amazon CloudWatch Logs configuration.

      - **fieldLogLevel** *(string) --*

        The field logging level. Values can be NONE, ERROR, or ALL.

        * **NONE** : No field-level logs are captured.

        * **ERROR** : Logs the following information only for the fields that are in error:

          * The error section in the server response.

          * Field-level errors.

          * The generated request/response functions that got resolved for error fields.

        * **ALL** : The following information is logged for all fields in the query:

          * Field-level tracing information.

          * The generated request/response functions that got resolved for each field.

      - **cloudWatchLogsRoleArn** *(string) --*

        The service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in your
        account.

      - **excludeVerboseContent** *(boolean) --*

        Set to TRUE to exclude sections that contain information such as headers, context, and
        evaluated mapping templates, regardless of logging level.

    - **userPoolConfig** *(dict) --*

      The Amazon Cognito user pool configuration.

      - **userPoolId** *(string) --*

        The user pool ID.

      - **awsRegion** *(string) --*

        The AWS Region in which the user pool was created.

      - **defaultAction** *(string) --*

        The action that you want your GraphQL API to take when a request that uses Amazon Cognito
        user pool authentication doesn't match the Amazon Cognito user pool configuration.

      - **appIdClientRegex** *(string) --*

        A regular expression for validating the incoming Amazon Cognito user pool app client ID.

    - **openIDConnectConfig** *(dict) --*

      The OpenID Connect configuration.

      - **issuer** *(string) --*

        The issuer for the OpenID Connect configuration. The issuer returned by discovery must
        exactly match the value of ``iss`` in the ID token.

      - **clientId** *(string) --*

        The client identifier of the Relying party at the OpenID identity provider. This identifier
        is typically obtained when the Relying party is registered with the OpenID identity
        provider. You can specify a regular expression so the AWS AppSync can validate against
        multiple client identifiers at a time.

      - **iatTTL** *(integer) --*

        The number of milliseconds a token is valid after being issued to a user.

      - **authTTL** *(integer) --*

        The number of milliseconds a token is valid after being authenticated.

    - **arn** *(string) --*

      The ARN.

    - **uris** *(dict) --*

      The URIs.

      - *(string) --*

        - *(string) --*

    - **tags** *(dict) --*

      The tags.

      - *(string) --*

        The key for the tag.

        - *(string) --*

          The value for the tag.

    - **additionalAuthenticationProviders** *(list) --*

      A list of additional authentication providers for the ``GraphqlApi`` API.

      - *(dict) --*

        Describes an additional authentication provider.

        - **authenticationType** *(string) --*

          The authentication type: API key, AWS IAM, OIDC, or Amazon Cognito user pools.

        - **openIDConnectConfig** *(dict) --*

          The OpenID Connect configuration.

          - **issuer** *(string) --*

            The issuer for the OpenID Connect configuration. The issuer returned by discovery must
            exactly match the value of ``iss`` in the ID token.

          - **clientId** *(string) --*

            The client identifier of the Relying party at the OpenID identity provider. This
            identifier is typically obtained when the Relying party is registered with the OpenID
            identity provider. You can specify a regular expression so the AWS AppSync can validate
            against multiple client identifiers at a time.

          - **iatTTL** *(integer) --*

            The number of milliseconds a token is valid after being issued to a user.

          - **authTTL** *(integer) --*

            The number of milliseconds a token is valid after being authenticated.

        - **userPoolConfig** *(dict) --*

          The Amazon Cognito user pool configuration.

          - **userPoolId** *(string) --*

            The user pool ID.

          - **awsRegion** *(string) --*

            The AWS Region in which the user pool was created.

          - **appIdClientRegex** *(string) --*

            A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientGetGraphqlApiResponseTypeDef = TypedDict(
    "_ClientGetGraphqlApiResponseTypeDef",
    {"graphqlApi": ClientGetGraphqlApiResponsegraphqlApiTypeDef},
    total=False,
)


class ClientGetGraphqlApiResponseTypeDef(_ClientGetGraphqlApiResponseTypeDef):
    """
    Type definition for `ClientGetGraphqlApi` `Response`

    - **graphqlApi** *(dict) --*

      The ``GraphqlApi`` object.

      - **name** *(string) --*

        The API name.

      - **apiId** *(string) --*

        The API ID.

      - **authenticationType** *(string) --*

        The authentication type.

      - **logConfig** *(dict) --*

        The Amazon CloudWatch Logs configuration.

        - **fieldLogLevel** *(string) --*

          The field logging level. Values can be NONE, ERROR, or ALL.

          * **NONE** : No field-level logs are captured.

          * **ERROR** : Logs the following information only for the fields that are in error:

            * The error section in the server response.

            * Field-level errors.

            * The generated request/response functions that got resolved for error fields.

          * **ALL** : The following information is logged for all fields in the query:

            * Field-level tracing information.

            * The generated request/response functions that got resolved for each field.

        - **cloudWatchLogsRoleArn** *(string) --*

          The service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in your
          account.

        - **excludeVerboseContent** *(boolean) --*

          Set to TRUE to exclude sections that contain information such as headers, context, and
          evaluated mapping templates, regardless of logging level.

      - **userPoolConfig** *(dict) --*

        The Amazon Cognito user pool configuration.

        - **userPoolId** *(string) --*

          The user pool ID.

        - **awsRegion** *(string) --*

          The AWS Region in which the user pool was created.

        - **defaultAction** *(string) --*

          The action that you want your GraphQL API to take when a request that uses Amazon Cognito
          user pool authentication doesn't match the Amazon Cognito user pool configuration.

        - **appIdClientRegex** *(string) --*

          A regular expression for validating the incoming Amazon Cognito user pool app client ID.

      - **openIDConnectConfig** *(dict) --*

        The OpenID Connect configuration.

        - **issuer** *(string) --*

          The issuer for the OpenID Connect configuration. The issuer returned by discovery must
          exactly match the value of ``iss`` in the ID token.

        - **clientId** *(string) --*

          The client identifier of the Relying party at the OpenID identity provider. This
          identifier is typically obtained when the Relying party is registered with the OpenID
          identity provider. You can specify a regular expression so the AWS AppSync can validate
          against multiple client identifiers at a time.

        - **iatTTL** *(integer) --*

          The number of milliseconds a token is valid after being issued to a user.

        - **authTTL** *(integer) --*

          The number of milliseconds a token is valid after being authenticated.

      - **arn** *(string) --*

        The ARN.

      - **uris** *(dict) --*

        The URIs.

        - *(string) --*

          - *(string) --*

      - **tags** *(dict) --*

        The tags.

        - *(string) --*

          The key for the tag.

          - *(string) --*

            The value for the tag.

      - **additionalAuthenticationProviders** *(list) --*

        A list of additional authentication providers for the ``GraphqlApi`` API.

        - *(dict) --*

          Describes an additional authentication provider.

          - **authenticationType** *(string) --*

            The authentication type: API key, AWS IAM, OIDC, or Amazon Cognito user pools.

          - **openIDConnectConfig** *(dict) --*

            The OpenID Connect configuration.

            - **issuer** *(string) --*

              The issuer for the OpenID Connect configuration. The issuer returned by discovery must
              exactly match the value of ``iss`` in the ID token.

            - **clientId** *(string) --*

              The client identifier of the Relying party at the OpenID identity provider. This
              identifier is typically obtained when the Relying party is registered with the OpenID
              identity provider. You can specify a regular expression so the AWS AppSync can
              validate against multiple client identifiers at a time.

            - **iatTTL** *(integer) --*

              The number of milliseconds a token is valid after being issued to a user.

            - **authTTL** *(integer) --*

              The number of milliseconds a token is valid after being authenticated.

          - **userPoolConfig** *(dict) --*

            The Amazon Cognito user pool configuration.

            - **userPoolId** *(string) --*

              The user pool ID.

            - **awsRegion** *(string) --*

              The AWS Region in which the user pool was created.

            - **appIdClientRegex** *(string) --*

              A regular expression for validating the incoming Amazon Cognito user pool app client
              ID.
    """


_ClientGetResolverResponseresolvercachingConfigTypeDef = TypedDict(
    "_ClientGetResolverResponseresolvercachingConfigTypeDef",
    {"ttl": int, "cachingKeys": List[str]},
    total=False,
)


class ClientGetResolverResponseresolvercachingConfigTypeDef(
    _ClientGetResolverResponseresolvercachingConfigTypeDef
):
    """
    Type definition for `ClientGetResolverResponseresolver` `cachingConfig`

    The caching configuration for the resolver.

    - **ttl** *(integer) --*

      The TTL in seconds for a resolver that has caching enabled.

      Valid values are between 1 and 3600 seconds.

    - **cachingKeys** *(list) --*

      The caching keys for a resolver that has caching enabled.

      Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

      - *(string) --*
    """


_ClientGetResolverResponseresolverpipelineConfigTypeDef = TypedDict(
    "_ClientGetResolverResponseresolverpipelineConfigTypeDef", {"functions": List[str]}, total=False
)


class ClientGetResolverResponseresolverpipelineConfigTypeDef(
    _ClientGetResolverResponseresolverpipelineConfigTypeDef
):
    """
    Type definition for `ClientGetResolverResponseresolver` `pipelineConfig`

    The ``PipelineConfig`` .

    - **functions** *(list) --*

      A list of ``Function`` objects.

      - *(string) --*
    """


_ClientGetResolverResponseresolversyncConfiglambdaConflictHandlerConfigTypeDef = TypedDict(
    "_ClientGetResolverResponseresolversyncConfiglambdaConflictHandlerConfigTypeDef",
    {"lambdaConflictHandlerArn": str},
    total=False,
)


class ClientGetResolverResponseresolversyncConfiglambdaConflictHandlerConfigTypeDef(
    _ClientGetResolverResponseresolversyncConfiglambdaConflictHandlerConfigTypeDef
):
    """
    Type definition for `ClientGetResolverResponseresolversyncConfig` `lambdaConflictHandlerConfig`

    The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

    - **lambdaConflictHandlerArn** *(string) --*

      The Arn for the Lambda function to use as the Conflict Handler.
    """


_ClientGetResolverResponseresolversyncConfigTypeDef = TypedDict(
    "_ClientGetResolverResponseresolversyncConfigTypeDef",
    {
        "conflictHandler": str,
        "conflictDetection": str,
        "lambdaConflictHandlerConfig": ClientGetResolverResponseresolversyncConfiglambdaConflictHandlerConfigTypeDef,
    },
    total=False,
)


class ClientGetResolverResponseresolversyncConfigTypeDef(
    _ClientGetResolverResponseresolversyncConfigTypeDef
):
    """
    Type definition for `ClientGetResolverResponseresolver` `syncConfig`

    The ``SyncConfig`` for a resolver attached to a versioned datasource.

    - **conflictHandler** *(string) --*

      The Conflict Resolution strategy to perform in the event of a conflict.

      * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do not
      match the latest version at the server.

      * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

      * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
      LambdaConflictHandlerConfig.

    - **conflictDetection** *(string) --*

      The Conflict Detection strategy to use.

      * **VERSION** : Detect conflicts based on object versions for this resolver.

      * **NONE** : Do not detect conflicts when executing this resolver.

    - **lambdaConflictHandlerConfig** *(dict) --*

      The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

      - **lambdaConflictHandlerArn** *(string) --*

        The Arn for the Lambda function to use as the Conflict Handler.
    """


_ClientGetResolverResponseresolverTypeDef = TypedDict(
    "_ClientGetResolverResponseresolverTypeDef",
    {
        "typeName": str,
        "fieldName": str,
        "dataSourceName": str,
        "resolverArn": str,
        "requestMappingTemplate": str,
        "responseMappingTemplate": str,
        "kind": str,
        "pipelineConfig": ClientGetResolverResponseresolverpipelineConfigTypeDef,
        "syncConfig": ClientGetResolverResponseresolversyncConfigTypeDef,
        "cachingConfig": ClientGetResolverResponseresolvercachingConfigTypeDef,
    },
    total=False,
)


class ClientGetResolverResponseresolverTypeDef(_ClientGetResolverResponseresolverTypeDef):
    """
    Type definition for `ClientGetResolverResponse` `resolver`

    The ``Resolver`` object.

    - **typeName** *(string) --*

      The resolver type name.

    - **fieldName** *(string) --*

      The resolver field name.

    - **dataSourceName** *(string) --*

      The resolver data source name.

    - **resolverArn** *(string) --*

      The resolver ARN.

    - **requestMappingTemplate** *(string) --*

      The request mapping template.

    - **responseMappingTemplate** *(string) --*

      The response mapping template.

    - **kind** *(string) --*

      The resolver type.

      * **UNIT** : A UNIT resolver type. A UNIT resolver is the default resolver type. A UNIT
      resolver enables you to execute a GraphQL query against a single data source.

      * **PIPELINE** : A PIPELINE resolver type. A PIPELINE resolver enables you to execute a series
      of ``Function`` in a serial manner. You can use a pipeline resolver to execute a GraphQL query
      against multiple data sources.

    - **pipelineConfig** *(dict) --*

      The ``PipelineConfig`` .

      - **functions** *(list) --*

        A list of ``Function`` objects.

        - *(string) --*

    - **syncConfig** *(dict) --*

      The ``SyncConfig`` for a resolver attached to a versioned datasource.

      - **conflictHandler** *(string) --*

        The Conflict Resolution strategy to perform in the event of a conflict.

        * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do not
        match the latest version at the server.

        * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

        * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
        LambdaConflictHandlerConfig.

      - **conflictDetection** *(string) --*

        The Conflict Detection strategy to use.

        * **VERSION** : Detect conflicts based on object versions for this resolver.

        * **NONE** : Do not detect conflicts when executing this resolver.

      - **lambdaConflictHandlerConfig** *(dict) --*

        The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

        - **lambdaConflictHandlerArn** *(string) --*

          The Arn for the Lambda function to use as the Conflict Handler.

    - **cachingConfig** *(dict) --*

      The caching configuration for the resolver.

      - **ttl** *(integer) --*

        The TTL in seconds for a resolver that has caching enabled.

        Valid values are between 1 and 3600 seconds.

      - **cachingKeys** *(list) --*

        The caching keys for a resolver that has caching enabled.

        Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

        - *(string) --*
    """


_ClientGetResolverResponseTypeDef = TypedDict(
    "_ClientGetResolverResponseTypeDef",
    {"resolver": ClientGetResolverResponseresolverTypeDef},
    total=False,
)


class ClientGetResolverResponseTypeDef(_ClientGetResolverResponseTypeDef):
    """
    Type definition for `ClientGetResolver` `Response`

    - **resolver** *(dict) --*

      The ``Resolver`` object.

      - **typeName** *(string) --*

        The resolver type name.

      - **fieldName** *(string) --*

        The resolver field name.

      - **dataSourceName** *(string) --*

        The resolver data source name.

      - **resolverArn** *(string) --*

        The resolver ARN.

      - **requestMappingTemplate** *(string) --*

        The request mapping template.

      - **responseMappingTemplate** *(string) --*

        The response mapping template.

      - **kind** *(string) --*

        The resolver type.

        * **UNIT** : A UNIT resolver type. A UNIT resolver is the default resolver type. A UNIT
        resolver enables you to execute a GraphQL query against a single data source.

        * **PIPELINE** : A PIPELINE resolver type. A PIPELINE resolver enables you to execute a
        series of ``Function`` in a serial manner. You can use a pipeline resolver to execute a
        GraphQL query against multiple data sources.

      - **pipelineConfig** *(dict) --*

        The ``PipelineConfig`` .

        - **functions** *(list) --*

          A list of ``Function`` objects.

          - *(string) --*

      - **syncConfig** *(dict) --*

        The ``SyncConfig`` for a resolver attached to a versioned datasource.

        - **conflictHandler** *(string) --*

          The Conflict Resolution strategy to perform in the event of a conflict.

          * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do
          not match the latest version at the server.

          * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

          * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
          LambdaConflictHandlerConfig.

        - **conflictDetection** *(string) --*

          The Conflict Detection strategy to use.

          * **VERSION** : Detect conflicts based on object versions for this resolver.

          * **NONE** : Do not detect conflicts when executing this resolver.

        - **lambdaConflictHandlerConfig** *(dict) --*

          The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

          - **lambdaConflictHandlerArn** *(string) --*

            The Arn for the Lambda function to use as the Conflict Handler.

      - **cachingConfig** *(dict) --*

        The caching configuration for the resolver.

        - **ttl** *(integer) --*

          The TTL in seconds for a resolver that has caching enabled.

          Valid values are between 1 and 3600 seconds.

        - **cachingKeys** *(list) --*

          The caching keys for a resolver that has caching enabled.

          Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

          - *(string) --*
    """


_ClientGetSchemaCreationStatusResponseTypeDef = TypedDict(
    "_ClientGetSchemaCreationStatusResponseTypeDef", {"status": str, "details": str}, total=False
)


class ClientGetSchemaCreationStatusResponseTypeDef(_ClientGetSchemaCreationStatusResponseTypeDef):
    """
    Type definition for `ClientGetSchemaCreationStatus` `Response`

    - **status** *(string) --*

      The current state of the schema (PROCESSING, FAILED, SUCCESS, or NOT_APPLICABLE). When the
      schema is in the ACTIVE state, you can add data.

    - **details** *(string) --*

      Detailed information about the status of the schema creation operation.
    """


_ClientGetTypeResponsetypeTypeDef = TypedDict(
    "_ClientGetTypeResponsetypeTypeDef",
    {"name": str, "description": str, "arn": str, "definition": str, "format": str},
    total=False,
)


class ClientGetTypeResponsetypeTypeDef(_ClientGetTypeResponsetypeTypeDef):
    """
    Type definition for `ClientGetTypeResponse` `type`

    The ``Type`` object.

    - **name** *(string) --*

      The type name.

    - **description** *(string) --*

      The type description.

    - **arn** *(string) --*

      The type ARN.

    - **definition** *(string) --*

      The type definition.

    - **format** *(string) --*

      The type format: SDL or JSON.
    """


_ClientGetTypeResponseTypeDef = TypedDict(
    "_ClientGetTypeResponseTypeDef", {"type": ClientGetTypeResponsetypeTypeDef}, total=False
)


class ClientGetTypeResponseTypeDef(_ClientGetTypeResponseTypeDef):
    """
    Type definition for `ClientGetType` `Response`

    - **type** *(dict) --*

      The ``Type`` object.

      - **name** *(string) --*

        The type name.

      - **description** *(string) --*

        The type description.

      - **arn** *(string) --*

        The type ARN.

      - **definition** *(string) --*

        The type definition.

      - **format** *(string) --*

        The type format: SDL or JSON.
    """


_ClientListApiKeysResponseapiKeysTypeDef = TypedDict(
    "_ClientListApiKeysResponseapiKeysTypeDef",
    {"id": str, "description": str, "expires": int},
    total=False,
)


class ClientListApiKeysResponseapiKeysTypeDef(_ClientListApiKeysResponseapiKeysTypeDef):
    """
    Type definition for `ClientListApiKeysResponse` `apiKeys`

    Describes an API key.

    Customers invoke AWS AppSync GraphQL API operations with API keys as an identity mechanism.
    There are two key versions:

     **da1** : This version was introduced at launch in November 2017. These keys always expire
     after 7 days. Key expiration is managed by Amazon DynamoDB TTL. The keys ceased to be valid
     after February 21, 2018 and should not be used after that date.

    * ``ListApiKeys`` returns the expiration time in milliseconds.

    * ``CreateApiKey`` returns the expiration time in milliseconds.

    * ``UpdateApiKey`` is not available for this key version.

    * ``DeleteApiKey`` deletes the item from the table.

    * Expiration is stored in Amazon DynamoDB as milliseconds. This results in a bug where keys are
    not automatically deleted because DynamoDB expects the TTL to be stored in seconds. As a
    one-time action, we will delete these keys from the table after February 21, 2018.

     **da2** : This version was introduced in February 2018 when AppSync added support to extend key
     expiration.

    * ``ListApiKeys`` returns the expiration time in seconds.

    * ``CreateApiKey`` returns the expiration time in seconds and accepts a user-provided expiration
    time in seconds.

    * ``UpdateApiKey`` returns the expiration time in seconds and accepts a user-provided expiration
    time in seconds. Key expiration can only be updated while the key has not expired.

    * ``DeleteApiKey`` deletes the item from the table.

    * Expiration is stored in Amazon DynamoDB as seconds.

    - **id** *(string) --*

      The API key ID.

    - **description** *(string) --*

      A description of the purpose of the API key.

    - **expires** *(integer) --*

      The time after which the API key expires. The date is represented as seconds since the epoch,
      rounded down to the nearest hour.
    """


_ClientListApiKeysResponseTypeDef = TypedDict(
    "_ClientListApiKeysResponseTypeDef",
    {"apiKeys": List[ClientListApiKeysResponseapiKeysTypeDef], "nextToken": str},
    total=False,
)


class ClientListApiKeysResponseTypeDef(_ClientListApiKeysResponseTypeDef):
    """
    Type definition for `ClientListApiKeys` `Response`

    - **apiKeys** *(list) --*

      The ``ApiKey`` objects.

      - *(dict) --*

        Describes an API key.

        Customers invoke AWS AppSync GraphQL API operations with API keys as an identity mechanism.
        There are two key versions:

         **da1** : This version was introduced at launch in November 2017. These keys always expire
         after 7 days. Key expiration is managed by Amazon DynamoDB TTL. The keys ceased to be valid
         after February 21, 2018 and should not be used after that date.

        * ``ListApiKeys`` returns the expiration time in milliseconds.

        * ``CreateApiKey`` returns the expiration time in milliseconds.

        * ``UpdateApiKey`` is not available for this key version.

        * ``DeleteApiKey`` deletes the item from the table.

        * Expiration is stored in Amazon DynamoDB as milliseconds. This results in a bug where keys
        are not automatically deleted because DynamoDB expects the TTL to be stored in seconds. As a
        one-time action, we will delete these keys from the table after February 21, 2018.

         **da2** : This version was introduced in February 2018 when AppSync added support to extend
         key expiration.

        * ``ListApiKeys`` returns the expiration time in seconds.

        * ``CreateApiKey`` returns the expiration time in seconds and accepts a user-provided
        expiration time in seconds.

        * ``UpdateApiKey`` returns the expiration time in seconds and accepts a user-provided
        expiration time in seconds. Key expiration can only be updated while the key has not
        expired.

        * ``DeleteApiKey`` deletes the item from the table.

        * Expiration is stored in Amazon DynamoDB as seconds.

        - **id** *(string) --*

          The API key ID.

        - **description** *(string) --*

          A description of the purpose of the API key.

        - **expires** *(integer) --*

          The time after which the API key expires. The date is represented as seconds since the
          epoch, rounded down to the nearest hour.

    - **nextToken** *(string) --*

      An identifier to be passed in the next request to this operation to return the next set of
      items in the list.
    """


_ClientListDataSourcesResponsedataSourcesdynamodbConfigdeltaSyncConfigTypeDef = TypedDict(
    "_ClientListDataSourcesResponsedataSourcesdynamodbConfigdeltaSyncConfigTypeDef",
    {"baseTableTTL": int, "deltaSyncTableName": str, "deltaSyncTableTTL": int},
    total=False,
)


class ClientListDataSourcesResponsedataSourcesdynamodbConfigdeltaSyncConfigTypeDef(
    _ClientListDataSourcesResponsedataSourcesdynamodbConfigdeltaSyncConfigTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponsedataSourcesdynamodbConfig` `deltaSyncConfig`

    The ``DeltaSyncConfig`` for a versioned datasource.

    - **baseTableTTL** *(integer) --*

      The number of minutes an Item is stored in the datasource.

    - **deltaSyncTableName** *(string) --*

      The Delta Sync table name.

    - **deltaSyncTableTTL** *(integer) --*

      The number of minutes a Delta Sync log entry is stored in the Delta Sync table.
    """


_ClientListDataSourcesResponsedataSourcesdynamodbConfigTypeDef = TypedDict(
    "_ClientListDataSourcesResponsedataSourcesdynamodbConfigTypeDef",
    {
        "tableName": str,
        "awsRegion": str,
        "useCallerCredentials": bool,
        "deltaSyncConfig": ClientListDataSourcesResponsedataSourcesdynamodbConfigdeltaSyncConfigTypeDef,
        "versioned": bool,
    },
    total=False,
)


class ClientListDataSourcesResponsedataSourcesdynamodbConfigTypeDef(
    _ClientListDataSourcesResponsedataSourcesdynamodbConfigTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponsedataSources` `dynamodbConfig`

    Amazon DynamoDB settings.

    - **tableName** *(string) --*

      The table name.

    - **awsRegion** *(string) --*

      The AWS Region.

    - **useCallerCredentials** *(boolean) --*

      Set to TRUE to use Amazon Cognito credentials with this data source.

    - **deltaSyncConfig** *(dict) --*

      The ``DeltaSyncConfig`` for a versioned datasource.

      - **baseTableTTL** *(integer) --*

        The number of minutes an Item is stored in the datasource.

      - **deltaSyncTableName** *(string) --*

        The Delta Sync table name.

      - **deltaSyncTableTTL** *(integer) --*

        The number of minutes a Delta Sync log entry is stored in the Delta Sync table.

    - **versioned** *(boolean) --*

      Set to TRUE to use Conflict Detection and Resolution with this data source.
    """


_ClientListDataSourcesResponsedataSourceselasticsearchConfigTypeDef = TypedDict(
    "_ClientListDataSourcesResponsedataSourceselasticsearchConfigTypeDef",
    {"endpoint": str, "awsRegion": str},
    total=False,
)


class ClientListDataSourcesResponsedataSourceselasticsearchConfigTypeDef(
    _ClientListDataSourcesResponsedataSourceselasticsearchConfigTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponsedataSources` `elasticsearchConfig`

    Amazon Elasticsearch Service settings.

    - **endpoint** *(string) --*

      The endpoint.

    - **awsRegion** *(string) --*

      The AWS Region.
    """


_ClientListDataSourcesResponsedataSourceshttpConfigauthorizationConfigawsIamConfigTypeDef = TypedDict(
    "_ClientListDataSourcesResponsedataSourceshttpConfigauthorizationConfigawsIamConfigTypeDef",
    {"signingRegion": str, "signingServiceName": str},
    total=False,
)


class ClientListDataSourcesResponsedataSourceshttpConfigauthorizationConfigawsIamConfigTypeDef(
    _ClientListDataSourcesResponsedataSourceshttpConfigauthorizationConfigawsIamConfigTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponsedataSourceshttpConfigauthorizationConfig`
    `awsIamConfig`

    The AWS IAM settings.

    - **signingRegion** *(string) --*

      The signing region for AWS IAM authorization.

    - **signingServiceName** *(string) --*

      The signing service name for AWS IAM authorization.
    """


_ClientListDataSourcesResponsedataSourceshttpConfigauthorizationConfigTypeDef = TypedDict(
    "_ClientListDataSourcesResponsedataSourceshttpConfigauthorizationConfigTypeDef",
    {
        "authorizationType": str,
        "awsIamConfig": ClientListDataSourcesResponsedataSourceshttpConfigauthorizationConfigawsIamConfigTypeDef,
    },
    total=False,
)


class ClientListDataSourcesResponsedataSourceshttpConfigauthorizationConfigTypeDef(
    _ClientListDataSourcesResponsedataSourceshttpConfigauthorizationConfigTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponsedataSourceshttpConfig` `authorizationConfig`

    The authorization config in case the HTTP endpoint requires authorization.

    - **authorizationType** *(string) --*

      The authorization type required by the HTTP endpoint.

      * **AWS_IAM** : The authorization type is Sigv4.

    - **awsIamConfig** *(dict) --*

      The AWS IAM settings.

      - **signingRegion** *(string) --*

        The signing region for AWS IAM authorization.

      - **signingServiceName** *(string) --*

        The signing service name for AWS IAM authorization.
    """


_ClientListDataSourcesResponsedataSourceshttpConfigTypeDef = TypedDict(
    "_ClientListDataSourcesResponsedataSourceshttpConfigTypeDef",
    {
        "endpoint": str,
        "authorizationConfig": ClientListDataSourcesResponsedataSourceshttpConfigauthorizationConfigTypeDef,
    },
    total=False,
)


class ClientListDataSourcesResponsedataSourceshttpConfigTypeDef(
    _ClientListDataSourcesResponsedataSourceshttpConfigTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponsedataSources` `httpConfig`

    HTTP endpoint settings.

    - **endpoint** *(string) --*

      The HTTP URL endpoint. You can either specify the domain name or IP, and port combination, and
      the URL scheme must be HTTP or HTTPS. If the port is not specified, AWS AppSync uses the
      default port 80 for the HTTP endpoint and port 443 for HTTPS endpoints.

    - **authorizationConfig** *(dict) --*

      The authorization config in case the HTTP endpoint requires authorization.

      - **authorizationType** *(string) --*

        The authorization type required by the HTTP endpoint.

        * **AWS_IAM** : The authorization type is Sigv4.

      - **awsIamConfig** *(dict) --*

        The AWS IAM settings.

        - **signingRegion** *(string) --*

          The signing region for AWS IAM authorization.

        - **signingServiceName** *(string) --*

          The signing service name for AWS IAM authorization.
    """


_ClientListDataSourcesResponsedataSourceslambdaConfigTypeDef = TypedDict(
    "_ClientListDataSourcesResponsedataSourceslambdaConfigTypeDef",
    {"lambdaFunctionArn": str},
    total=False,
)


class ClientListDataSourcesResponsedataSourceslambdaConfigTypeDef(
    _ClientListDataSourcesResponsedataSourceslambdaConfigTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponsedataSources` `lambdaConfig`

    AWS Lambda settings.

    - **lambdaFunctionArn** *(string) --*

      The ARN for the Lambda function.
    """


_ClientListDataSourcesResponsedataSourcesrelationalDatabaseConfigrdsHttpEndpointConfigTypeDef = TypedDict(
    "_ClientListDataSourcesResponsedataSourcesrelationalDatabaseConfigrdsHttpEndpointConfigTypeDef",
    {
        "awsRegion": str,
        "dbClusterIdentifier": str,
        "databaseName": str,
        "schema": str,
        "awsSecretStoreArn": str,
    },
    total=False,
)


class ClientListDataSourcesResponsedataSourcesrelationalDatabaseConfigrdsHttpEndpointConfigTypeDef(
    _ClientListDataSourcesResponsedataSourcesrelationalDatabaseConfigrdsHttpEndpointConfigTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponsedataSourcesrelationalDatabaseConfig`
    `rdsHttpEndpointConfig`

    Amazon RDS HTTP endpoint settings.

    - **awsRegion** *(string) --*

      AWS Region for RDS HTTP endpoint.

    - **dbClusterIdentifier** *(string) --*

      Amazon RDS cluster identifier.

    - **databaseName** *(string) --*

      Logical database name.

    - **schema** *(string) --*

      Logical schema name.

    - **awsSecretStoreArn** *(string) --*

      AWS secret store ARN for database credentials.
    """


_ClientListDataSourcesResponsedataSourcesrelationalDatabaseConfigTypeDef = TypedDict(
    "_ClientListDataSourcesResponsedataSourcesrelationalDatabaseConfigTypeDef",
    {
        "relationalDatabaseSourceType": str,
        "rdsHttpEndpointConfig": ClientListDataSourcesResponsedataSourcesrelationalDatabaseConfigrdsHttpEndpointConfigTypeDef,
    },
    total=False,
)


class ClientListDataSourcesResponsedataSourcesrelationalDatabaseConfigTypeDef(
    _ClientListDataSourcesResponsedataSourcesrelationalDatabaseConfigTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponsedataSources` `relationalDatabaseConfig`

    Relational database settings.

    - **relationalDatabaseSourceType** *(string) --*

      Source type for the relational database.

      * **RDS_HTTP_ENDPOINT** : The relational database source type is an Amazon RDS HTTP endpoint.

    - **rdsHttpEndpointConfig** *(dict) --*

      Amazon RDS HTTP endpoint settings.

      - **awsRegion** *(string) --*

        AWS Region for RDS HTTP endpoint.

      - **dbClusterIdentifier** *(string) --*

        Amazon RDS cluster identifier.

      - **databaseName** *(string) --*

        Logical database name.

      - **schema** *(string) --*

        Logical schema name.

      - **awsSecretStoreArn** *(string) --*

        AWS secret store ARN for database credentials.
    """


_ClientListDataSourcesResponsedataSourcesTypeDef = TypedDict(
    "_ClientListDataSourcesResponsedataSourcesTypeDef",
    {
        "dataSourceArn": str,
        "name": str,
        "description": str,
        "type": str,
        "serviceRoleArn": str,
        "dynamodbConfig": ClientListDataSourcesResponsedataSourcesdynamodbConfigTypeDef,
        "lambdaConfig": ClientListDataSourcesResponsedataSourceslambdaConfigTypeDef,
        "elasticsearchConfig": ClientListDataSourcesResponsedataSourceselasticsearchConfigTypeDef,
        "httpConfig": ClientListDataSourcesResponsedataSourceshttpConfigTypeDef,
        "relationalDatabaseConfig": ClientListDataSourcesResponsedataSourcesrelationalDatabaseConfigTypeDef,
    },
    total=False,
)


class ClientListDataSourcesResponsedataSourcesTypeDef(
    _ClientListDataSourcesResponsedataSourcesTypeDef
):
    """
    Type definition for `ClientListDataSourcesResponse` `dataSources`

    Describes a data source.

    - **dataSourceArn** *(string) --*

      The data source ARN.

    - **name** *(string) --*

      The name of the data source.

    - **description** *(string) --*

      The description of the data source.

    - **type** *(string) --*

      The type of the data source.

      * **AMAZON_DYNAMODB** : The data source is an Amazon DynamoDB table.

      * **AMAZON_ELASTICSEARCH** : The data source is an Amazon Elasticsearch Service domain.

      * **AWS_LAMBDA** : The data source is an AWS Lambda function.

      * **NONE** : There is no data source. This type is used when you wish to invoke a GraphQL
      operation without connecting to a data source, such as performing data transformation with
      resolvers or triggering a subscription to be invoked from a mutation.

      * **HTTP** : The data source is an HTTP endpoint.

      * **RELATIONAL_DATABASE** : The data source is a relational database.

    - **serviceRoleArn** *(string) --*

      The AWS IAM service role ARN for the data source. The system assumes this role when accessing
      the data source.

    - **dynamodbConfig** *(dict) --*

      Amazon DynamoDB settings.

      - **tableName** *(string) --*

        The table name.

      - **awsRegion** *(string) --*

        The AWS Region.

      - **useCallerCredentials** *(boolean) --*

        Set to TRUE to use Amazon Cognito credentials with this data source.

      - **deltaSyncConfig** *(dict) --*

        The ``DeltaSyncConfig`` for a versioned datasource.

        - **baseTableTTL** *(integer) --*

          The number of minutes an Item is stored in the datasource.

        - **deltaSyncTableName** *(string) --*

          The Delta Sync table name.

        - **deltaSyncTableTTL** *(integer) --*

          The number of minutes a Delta Sync log entry is stored in the Delta Sync table.

      - **versioned** *(boolean) --*

        Set to TRUE to use Conflict Detection and Resolution with this data source.

    - **lambdaConfig** *(dict) --*

      AWS Lambda settings.

      - **lambdaFunctionArn** *(string) --*

        The ARN for the Lambda function.

    - **elasticsearchConfig** *(dict) --*

      Amazon Elasticsearch Service settings.

      - **endpoint** *(string) --*

        The endpoint.

      - **awsRegion** *(string) --*

        The AWS Region.

    - **httpConfig** *(dict) --*

      HTTP endpoint settings.

      - **endpoint** *(string) --*

        The HTTP URL endpoint. You can either specify the domain name or IP, and port combination,
        and the URL scheme must be HTTP or HTTPS. If the port is not specified, AWS AppSync uses the
        default port 80 for the HTTP endpoint and port 443 for HTTPS endpoints.

      - **authorizationConfig** *(dict) --*

        The authorization config in case the HTTP endpoint requires authorization.

        - **authorizationType** *(string) --*

          The authorization type required by the HTTP endpoint.

          * **AWS_IAM** : The authorization type is Sigv4.

        - **awsIamConfig** *(dict) --*

          The AWS IAM settings.

          - **signingRegion** *(string) --*

            The signing region for AWS IAM authorization.

          - **signingServiceName** *(string) --*

            The signing service name for AWS IAM authorization.

    - **relationalDatabaseConfig** *(dict) --*

      Relational database settings.

      - **relationalDatabaseSourceType** *(string) --*

        Source type for the relational database.

        * **RDS_HTTP_ENDPOINT** : The relational database source type is an Amazon RDS HTTP
        endpoint.

      - **rdsHttpEndpointConfig** *(dict) --*

        Amazon RDS HTTP endpoint settings.

        - **awsRegion** *(string) --*

          AWS Region for RDS HTTP endpoint.

        - **dbClusterIdentifier** *(string) --*

          Amazon RDS cluster identifier.

        - **databaseName** *(string) --*

          Logical database name.

        - **schema** *(string) --*

          Logical schema name.

        - **awsSecretStoreArn** *(string) --*

          AWS secret store ARN for database credentials.
    """


_ClientListDataSourcesResponseTypeDef = TypedDict(
    "_ClientListDataSourcesResponseTypeDef",
    {"dataSources": List[ClientListDataSourcesResponsedataSourcesTypeDef], "nextToken": str},
    total=False,
)


class ClientListDataSourcesResponseTypeDef(_ClientListDataSourcesResponseTypeDef):
    """
    Type definition for `ClientListDataSources` `Response`

    - **dataSources** *(list) --*

      The ``DataSource`` objects.

      - *(dict) --*

        Describes a data source.

        - **dataSourceArn** *(string) --*

          The data source ARN.

        - **name** *(string) --*

          The name of the data source.

        - **description** *(string) --*

          The description of the data source.

        - **type** *(string) --*

          The type of the data source.

          * **AMAZON_DYNAMODB** : The data source is an Amazon DynamoDB table.

          * **AMAZON_ELASTICSEARCH** : The data source is an Amazon Elasticsearch Service domain.

          * **AWS_LAMBDA** : The data source is an AWS Lambda function.

          * **NONE** : There is no data source. This type is used when you wish to invoke a GraphQL
          operation without connecting to a data source, such as performing data transformation with
          resolvers or triggering a subscription to be invoked from a mutation.

          * **HTTP** : The data source is an HTTP endpoint.

          * **RELATIONAL_DATABASE** : The data source is a relational database.

        - **serviceRoleArn** *(string) --*

          The AWS IAM service role ARN for the data source. The system assumes this role when
          accessing the data source.

        - **dynamodbConfig** *(dict) --*

          Amazon DynamoDB settings.

          - **tableName** *(string) --*

            The table name.

          - **awsRegion** *(string) --*

            The AWS Region.

          - **useCallerCredentials** *(boolean) --*

            Set to TRUE to use Amazon Cognito credentials with this data source.

          - **deltaSyncConfig** *(dict) --*

            The ``DeltaSyncConfig`` for a versioned datasource.

            - **baseTableTTL** *(integer) --*

              The number of minutes an Item is stored in the datasource.

            - **deltaSyncTableName** *(string) --*

              The Delta Sync table name.

            - **deltaSyncTableTTL** *(integer) --*

              The number of minutes a Delta Sync log entry is stored in the Delta Sync table.

          - **versioned** *(boolean) --*

            Set to TRUE to use Conflict Detection and Resolution with this data source.

        - **lambdaConfig** *(dict) --*

          AWS Lambda settings.

          - **lambdaFunctionArn** *(string) --*

            The ARN for the Lambda function.

        - **elasticsearchConfig** *(dict) --*

          Amazon Elasticsearch Service settings.

          - **endpoint** *(string) --*

            The endpoint.

          - **awsRegion** *(string) --*

            The AWS Region.

        - **httpConfig** *(dict) --*

          HTTP endpoint settings.

          - **endpoint** *(string) --*

            The HTTP URL endpoint. You can either specify the domain name or IP, and port
            combination, and the URL scheme must be HTTP or HTTPS. If the port is not specified, AWS
            AppSync uses the default port 80 for the HTTP endpoint and port 443 for HTTPS endpoints.

          - **authorizationConfig** *(dict) --*

            The authorization config in case the HTTP endpoint requires authorization.

            - **authorizationType** *(string) --*

              The authorization type required by the HTTP endpoint.

              * **AWS_IAM** : The authorization type is Sigv4.

            - **awsIamConfig** *(dict) --*

              The AWS IAM settings.

              - **signingRegion** *(string) --*

                The signing region for AWS IAM authorization.

              - **signingServiceName** *(string) --*

                The signing service name for AWS IAM authorization.

        - **relationalDatabaseConfig** *(dict) --*

          Relational database settings.

          - **relationalDatabaseSourceType** *(string) --*

            Source type for the relational database.

            * **RDS_HTTP_ENDPOINT** : The relational database source type is an Amazon RDS HTTP
            endpoint.

          - **rdsHttpEndpointConfig** *(dict) --*

            Amazon RDS HTTP endpoint settings.

            - **awsRegion** *(string) --*

              AWS Region for RDS HTTP endpoint.

            - **dbClusterIdentifier** *(string) --*

              Amazon RDS cluster identifier.

            - **databaseName** *(string) --*

              Logical database name.

            - **schema** *(string) --*

              Logical schema name.

            - **awsSecretStoreArn** *(string) --*

              AWS secret store ARN for database credentials.

    - **nextToken** *(string) --*

      An identifier to be passed in the next request to this operation to return the next set of
      items in the list.
    """


_ClientListFunctionsResponsefunctionsTypeDef = TypedDict(
    "_ClientListFunctionsResponsefunctionsTypeDef",
    {
        "functionId": str,
        "functionArn": str,
        "name": str,
        "description": str,
        "dataSourceName": str,
        "requestMappingTemplate": str,
        "responseMappingTemplate": str,
        "functionVersion": str,
    },
    total=False,
)


class ClientListFunctionsResponsefunctionsTypeDef(_ClientListFunctionsResponsefunctionsTypeDef):
    """
    Type definition for `ClientListFunctionsResponse` `functions`

    A function is a reusable entity. Multiple functions can be used to compose the resolver logic.

    - **functionId** *(string) --*

      A unique ID representing the ``Function`` object.

    - **functionArn** *(string) --*

      The ARN of the ``Function`` object.

    - **name** *(string) --*

      The name of the ``Function`` object.

    - **description** *(string) --*

      The ``Function`` description.

    - **dataSourceName** *(string) --*

      The name of the ``DataSource`` .

    - **requestMappingTemplate** *(string) --*

      The ``Function`` request mapping template. Functions support only the 2018-05-29 version of
      the request mapping template.

    - **responseMappingTemplate** *(string) --*

      The ``Function`` response mapping template.

    - **functionVersion** *(string) --*

      The version of the request mapping template. Currently only the 2018-05-29 version of the
      template is supported.
    """


_ClientListFunctionsResponseTypeDef = TypedDict(
    "_ClientListFunctionsResponseTypeDef",
    {"functions": List[ClientListFunctionsResponsefunctionsTypeDef], "nextToken": str},
    total=False,
)


class ClientListFunctionsResponseTypeDef(_ClientListFunctionsResponseTypeDef):
    """
    Type definition for `ClientListFunctions` `Response`

    - **functions** *(list) --*

      A list of ``Function`` objects.

      - *(dict) --*

        A function is a reusable entity. Multiple functions can be used to compose the resolver
        logic.

        - **functionId** *(string) --*

          A unique ID representing the ``Function`` object.

        - **functionArn** *(string) --*

          The ARN of the ``Function`` object.

        - **name** *(string) --*

          The name of the ``Function`` object.

        - **description** *(string) --*

          The ``Function`` description.

        - **dataSourceName** *(string) --*

          The name of the ``DataSource`` .

        - **requestMappingTemplate** *(string) --*

          The ``Function`` request mapping template. Functions support only the 2018-05-29 version
          of the request mapping template.

        - **responseMappingTemplate** *(string) --*

          The ``Function`` response mapping template.

        - **functionVersion** *(string) --*

          The version of the request mapping template. Currently only the 2018-05-29 version of the
          template is supported.

    - **nextToken** *(string) --*

      An identifier that was returned from the previous call to this operation, which can be used to
      return the next set of items in the list.
    """


_ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProvidersopenIDConnectConfigTypeDef = TypedDict(
    "_ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProvidersopenIDConnectConfigTypeDef",
    {"issuer": str, "clientId": str, "iatTTL": int, "authTTL": int},
    total=False,
)


class ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProvidersopenIDConnectConfigTypeDef(
    _ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProvidersopenIDConnectConfigTypeDef
):
    """
    Type definition for `ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProviders`
    `openIDConnectConfig`

    The OpenID Connect configuration.

    - **issuer** *(string) --*

      The issuer for the OpenID Connect configuration. The issuer returned by discovery must exactly
      match the value of ``iss`` in the ID token.

    - **clientId** *(string) --*

      The client identifier of the Relying party at the OpenID identity provider. This identifier is
      typically obtained when the Relying party is registered with the OpenID identity provider. You
      can specify a regular expression so the AWS AppSync can validate against multiple client
      identifiers at a time.

    - **iatTTL** *(integer) --*

      The number of milliseconds a token is valid after being issued to a user.

    - **authTTL** *(integer) --*

      The number of milliseconds a token is valid after being authenticated.
    """


_ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProvidersuserPoolConfigTypeDef = TypedDict(
    "_ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProvidersuserPoolConfigTypeDef",
    {"userPoolId": str, "awsRegion": str, "appIdClientRegex": str},
    total=False,
)


class ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProvidersuserPoolConfigTypeDef(
    _ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProvidersuserPoolConfigTypeDef
):
    """
    Type definition for `ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProviders`
    `userPoolConfig`

    The Amazon Cognito user pool configuration.

    - **userPoolId** *(string) --*

      The user pool ID.

    - **awsRegion** *(string) --*

      The AWS Region in which the user pool was created.

    - **appIdClientRegex** *(string) --*

      A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProvidersTypeDef = TypedDict(
    "_ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProvidersTypeDef",
    {
        "authenticationType": str,
        "openIDConnectConfig": ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProvidersopenIDConnectConfigTypeDef,
        "userPoolConfig": ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProvidersuserPoolConfigTypeDef,
    },
    total=False,
)


class ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProvidersTypeDef(
    _ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProvidersTypeDef
):
    """
    Type definition for `ClientListGraphqlApisResponsegraphqlApis`
    `additionalAuthenticationProviders`

    Describes an additional authentication provider.

    - **authenticationType** *(string) --*

      The authentication type: API key, AWS IAM, OIDC, or Amazon Cognito user pools.

    - **openIDConnectConfig** *(dict) --*

      The OpenID Connect configuration.

      - **issuer** *(string) --*

        The issuer for the OpenID Connect configuration. The issuer returned by discovery must
        exactly match the value of ``iss`` in the ID token.

      - **clientId** *(string) --*

        The client identifier of the Relying party at the OpenID identity provider. This identifier
        is typically obtained when the Relying party is registered with the OpenID identity
        provider. You can specify a regular expression so the AWS AppSync can validate against
        multiple client identifiers at a time.

      - **iatTTL** *(integer) --*

        The number of milliseconds a token is valid after being issued to a user.

      - **authTTL** *(integer) --*

        The number of milliseconds a token is valid after being authenticated.

    - **userPoolConfig** *(dict) --*

      The Amazon Cognito user pool configuration.

      - **userPoolId** *(string) --*

        The user pool ID.

      - **awsRegion** *(string) --*

        The AWS Region in which the user pool was created.

      - **appIdClientRegex** *(string) --*

        A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientListGraphqlApisResponsegraphqlApislogConfigTypeDef = TypedDict(
    "_ClientListGraphqlApisResponsegraphqlApislogConfigTypeDef",
    {"fieldLogLevel": str, "cloudWatchLogsRoleArn": str, "excludeVerboseContent": bool},
    total=False,
)


class ClientListGraphqlApisResponsegraphqlApislogConfigTypeDef(
    _ClientListGraphqlApisResponsegraphqlApislogConfigTypeDef
):
    """
    Type definition for `ClientListGraphqlApisResponsegraphqlApis` `logConfig`

    The Amazon CloudWatch Logs configuration.

    - **fieldLogLevel** *(string) --*

      The field logging level. Values can be NONE, ERROR, or ALL.

      * **NONE** : No field-level logs are captured.

      * **ERROR** : Logs the following information only for the fields that are in error:

        * The error section in the server response.

        * Field-level errors.

        * The generated request/response functions that got resolved for error fields.

      * **ALL** : The following information is logged for all fields in the query:

        * Field-level tracing information.

        * The generated request/response functions that got resolved for each field.

    - **cloudWatchLogsRoleArn** *(string) --*

      The service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in your
      account.

    - **excludeVerboseContent** *(boolean) --*

      Set to TRUE to exclude sections that contain information such as headers, context, and
      evaluated mapping templates, regardless of logging level.
    """


_ClientListGraphqlApisResponsegraphqlApisopenIDConnectConfigTypeDef = TypedDict(
    "_ClientListGraphqlApisResponsegraphqlApisopenIDConnectConfigTypeDef",
    {"issuer": str, "clientId": str, "iatTTL": int, "authTTL": int},
    total=False,
)


class ClientListGraphqlApisResponsegraphqlApisopenIDConnectConfigTypeDef(
    _ClientListGraphqlApisResponsegraphqlApisopenIDConnectConfigTypeDef
):
    """
    Type definition for `ClientListGraphqlApisResponsegraphqlApis` `openIDConnectConfig`

    The OpenID Connect configuration.

    - **issuer** *(string) --*

      The issuer for the OpenID Connect configuration. The issuer returned by discovery must exactly
      match the value of ``iss`` in the ID token.

    - **clientId** *(string) --*

      The client identifier of the Relying party at the OpenID identity provider. This identifier is
      typically obtained when the Relying party is registered with the OpenID identity provider. You
      can specify a regular expression so the AWS AppSync can validate against multiple client
      identifiers at a time.

    - **iatTTL** *(integer) --*

      The number of milliseconds a token is valid after being issued to a user.

    - **authTTL** *(integer) --*

      The number of milliseconds a token is valid after being authenticated.
    """


_ClientListGraphqlApisResponsegraphqlApisuserPoolConfigTypeDef = TypedDict(
    "_ClientListGraphqlApisResponsegraphqlApisuserPoolConfigTypeDef",
    {"userPoolId": str, "awsRegion": str, "defaultAction": str, "appIdClientRegex": str},
    total=False,
)


class ClientListGraphqlApisResponsegraphqlApisuserPoolConfigTypeDef(
    _ClientListGraphqlApisResponsegraphqlApisuserPoolConfigTypeDef
):
    """
    Type definition for `ClientListGraphqlApisResponsegraphqlApis` `userPoolConfig`

    The Amazon Cognito user pool configuration.

    - **userPoolId** *(string) --*

      The user pool ID.

    - **awsRegion** *(string) --*

      The AWS Region in which the user pool was created.

    - **defaultAction** *(string) --*

      The action that you want your GraphQL API to take when a request that uses Amazon Cognito user
      pool authentication doesn't match the Amazon Cognito user pool configuration.

    - **appIdClientRegex** *(string) --*

      A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientListGraphqlApisResponsegraphqlApisTypeDef = TypedDict(
    "_ClientListGraphqlApisResponsegraphqlApisTypeDef",
    {
        "name": str,
        "apiId": str,
        "authenticationType": str,
        "logConfig": ClientListGraphqlApisResponsegraphqlApislogConfigTypeDef,
        "userPoolConfig": ClientListGraphqlApisResponsegraphqlApisuserPoolConfigTypeDef,
        "openIDConnectConfig": ClientListGraphqlApisResponsegraphqlApisopenIDConnectConfigTypeDef,
        "arn": str,
        "uris": Dict[str, str],
        "tags": Dict[str, str],
        "additionalAuthenticationProviders": List[
            ClientListGraphqlApisResponsegraphqlApisadditionalAuthenticationProvidersTypeDef
        ],
    },
    total=False,
)


class ClientListGraphqlApisResponsegraphqlApisTypeDef(
    _ClientListGraphqlApisResponsegraphqlApisTypeDef
):
    """
    Type definition for `ClientListGraphqlApisResponse` `graphqlApis`

    Describes a GraphQL API.

    - **name** *(string) --*

      The API name.

    - **apiId** *(string) --*

      The API ID.

    - **authenticationType** *(string) --*

      The authentication type.

    - **logConfig** *(dict) --*

      The Amazon CloudWatch Logs configuration.

      - **fieldLogLevel** *(string) --*

        The field logging level. Values can be NONE, ERROR, or ALL.

        * **NONE** : No field-level logs are captured.

        * **ERROR** : Logs the following information only for the fields that are in error:

          * The error section in the server response.

          * Field-level errors.

          * The generated request/response functions that got resolved for error fields.

        * **ALL** : The following information is logged for all fields in the query:

          * Field-level tracing information.

          * The generated request/response functions that got resolved for each field.

      - **cloudWatchLogsRoleArn** *(string) --*

        The service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in your
        account.

      - **excludeVerboseContent** *(boolean) --*

        Set to TRUE to exclude sections that contain information such as headers, context, and
        evaluated mapping templates, regardless of logging level.

    - **userPoolConfig** *(dict) --*

      The Amazon Cognito user pool configuration.

      - **userPoolId** *(string) --*

        The user pool ID.

      - **awsRegion** *(string) --*

        The AWS Region in which the user pool was created.

      - **defaultAction** *(string) --*

        The action that you want your GraphQL API to take when a request that uses Amazon Cognito
        user pool authentication doesn't match the Amazon Cognito user pool configuration.

      - **appIdClientRegex** *(string) --*

        A regular expression for validating the incoming Amazon Cognito user pool app client ID.

    - **openIDConnectConfig** *(dict) --*

      The OpenID Connect configuration.

      - **issuer** *(string) --*

        The issuer for the OpenID Connect configuration. The issuer returned by discovery must
        exactly match the value of ``iss`` in the ID token.

      - **clientId** *(string) --*

        The client identifier of the Relying party at the OpenID identity provider. This identifier
        is typically obtained when the Relying party is registered with the OpenID identity
        provider. You can specify a regular expression so the AWS AppSync can validate against
        multiple client identifiers at a time.

      - **iatTTL** *(integer) --*

        The number of milliseconds a token is valid after being issued to a user.

      - **authTTL** *(integer) --*

        The number of milliseconds a token is valid after being authenticated.

    - **arn** *(string) --*

      The ARN.

    - **uris** *(dict) --*

      The URIs.

      - *(string) --*

        - *(string) --*

    - **tags** *(dict) --*

      The tags.

      - *(string) --*

        The key for the tag.

        - *(string) --*

          The value for the tag.

    - **additionalAuthenticationProviders** *(list) --*

      A list of additional authentication providers for the ``GraphqlApi`` API.

      - *(dict) --*

        Describes an additional authentication provider.

        - **authenticationType** *(string) --*

          The authentication type: API key, AWS IAM, OIDC, or Amazon Cognito user pools.

        - **openIDConnectConfig** *(dict) --*

          The OpenID Connect configuration.

          - **issuer** *(string) --*

            The issuer for the OpenID Connect configuration. The issuer returned by discovery must
            exactly match the value of ``iss`` in the ID token.

          - **clientId** *(string) --*

            The client identifier of the Relying party at the OpenID identity provider. This
            identifier is typically obtained when the Relying party is registered with the OpenID
            identity provider. You can specify a regular expression so the AWS AppSync can validate
            against multiple client identifiers at a time.

          - **iatTTL** *(integer) --*

            The number of milliseconds a token is valid after being issued to a user.

          - **authTTL** *(integer) --*

            The number of milliseconds a token is valid after being authenticated.

        - **userPoolConfig** *(dict) --*

          The Amazon Cognito user pool configuration.

          - **userPoolId** *(string) --*

            The user pool ID.

          - **awsRegion** *(string) --*

            The AWS Region in which the user pool was created.

          - **appIdClientRegex** *(string) --*

            A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientListGraphqlApisResponseTypeDef = TypedDict(
    "_ClientListGraphqlApisResponseTypeDef",
    {"graphqlApis": List[ClientListGraphqlApisResponsegraphqlApisTypeDef], "nextToken": str},
    total=False,
)


class ClientListGraphqlApisResponseTypeDef(_ClientListGraphqlApisResponseTypeDef):
    """
    Type definition for `ClientListGraphqlApis` `Response`

    - **graphqlApis** *(list) --*

      The ``GraphqlApi`` objects.

      - *(dict) --*

        Describes a GraphQL API.

        - **name** *(string) --*

          The API name.

        - **apiId** *(string) --*

          The API ID.

        - **authenticationType** *(string) --*

          The authentication type.

        - **logConfig** *(dict) --*

          The Amazon CloudWatch Logs configuration.

          - **fieldLogLevel** *(string) --*

            The field logging level. Values can be NONE, ERROR, or ALL.

            * **NONE** : No field-level logs are captured.

            * **ERROR** : Logs the following information only for the fields that are in error:

              * The error section in the server response.

              * Field-level errors.

              * The generated request/response functions that got resolved for error fields.

            * **ALL** : The following information is logged for all fields in the query:

              * Field-level tracing information.

              * The generated request/response functions that got resolved for each field.

          - **cloudWatchLogsRoleArn** *(string) --*

            The service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in
            your account.

          - **excludeVerboseContent** *(boolean) --*

            Set to TRUE to exclude sections that contain information such as headers, context, and
            evaluated mapping templates, regardless of logging level.

        - **userPoolConfig** *(dict) --*

          The Amazon Cognito user pool configuration.

          - **userPoolId** *(string) --*

            The user pool ID.

          - **awsRegion** *(string) --*

            The AWS Region in which the user pool was created.

          - **defaultAction** *(string) --*

            The action that you want your GraphQL API to take when a request that uses Amazon
            Cognito user pool authentication doesn't match the Amazon Cognito user pool
            configuration.

          - **appIdClientRegex** *(string) --*

            A regular expression for validating the incoming Amazon Cognito user pool app client ID.

        - **openIDConnectConfig** *(dict) --*

          The OpenID Connect configuration.

          - **issuer** *(string) --*

            The issuer for the OpenID Connect configuration. The issuer returned by discovery must
            exactly match the value of ``iss`` in the ID token.

          - **clientId** *(string) --*

            The client identifier of the Relying party at the OpenID identity provider. This
            identifier is typically obtained when the Relying party is registered with the OpenID
            identity provider. You can specify a regular expression so the AWS AppSync can validate
            against multiple client identifiers at a time.

          - **iatTTL** *(integer) --*

            The number of milliseconds a token is valid after being issued to a user.

          - **authTTL** *(integer) --*

            The number of milliseconds a token is valid after being authenticated.

        - **arn** *(string) --*

          The ARN.

        - **uris** *(dict) --*

          The URIs.

          - *(string) --*

            - *(string) --*

        - **tags** *(dict) --*

          The tags.

          - *(string) --*

            The key for the tag.

            - *(string) --*

              The value for the tag.

        - **additionalAuthenticationProviders** *(list) --*

          A list of additional authentication providers for the ``GraphqlApi`` API.

          - *(dict) --*

            Describes an additional authentication provider.

            - **authenticationType** *(string) --*

              The authentication type: API key, AWS IAM, OIDC, or Amazon Cognito user pools.

            - **openIDConnectConfig** *(dict) --*

              The OpenID Connect configuration.

              - **issuer** *(string) --*

                The issuer for the OpenID Connect configuration. The issuer returned by discovery
                must exactly match the value of ``iss`` in the ID token.

              - **clientId** *(string) --*

                The client identifier of the Relying party at the OpenID identity provider. This
                identifier is typically obtained when the Relying party is registered with the
                OpenID identity provider. You can specify a regular expression so the AWS AppSync
                can validate against multiple client identifiers at a time.

              - **iatTTL** *(integer) --*

                The number of milliseconds a token is valid after being issued to a user.

              - **authTTL** *(integer) --*

                The number of milliseconds a token is valid after being authenticated.

            - **userPoolConfig** *(dict) --*

              The Amazon Cognito user pool configuration.

              - **userPoolId** *(string) --*

                The user pool ID.

              - **awsRegion** *(string) --*

                The AWS Region in which the user pool was created.

              - **appIdClientRegex** *(string) --*

                A regular expression for validating the incoming Amazon Cognito user pool app client
                ID.

    - **nextToken** *(string) --*

      An identifier to be passed in the next request to this operation to return the next set of
      items in the list.
    """


_ClientListResolversByFunctionResponseresolverscachingConfigTypeDef = TypedDict(
    "_ClientListResolversByFunctionResponseresolverscachingConfigTypeDef",
    {"ttl": int, "cachingKeys": List[str]},
    total=False,
)


class ClientListResolversByFunctionResponseresolverscachingConfigTypeDef(
    _ClientListResolversByFunctionResponseresolverscachingConfigTypeDef
):
    """
    Type definition for `ClientListResolversByFunctionResponseresolvers` `cachingConfig`

    The caching configuration for the resolver.

    - **ttl** *(integer) --*

      The TTL in seconds for a resolver that has caching enabled.

      Valid values are between 1 and 3600 seconds.

    - **cachingKeys** *(list) --*

      The caching keys for a resolver that has caching enabled.

      Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

      - *(string) --*
    """


_ClientListResolversByFunctionResponseresolverspipelineConfigTypeDef = TypedDict(
    "_ClientListResolversByFunctionResponseresolverspipelineConfigTypeDef",
    {"functions": List[str]},
    total=False,
)


class ClientListResolversByFunctionResponseresolverspipelineConfigTypeDef(
    _ClientListResolversByFunctionResponseresolverspipelineConfigTypeDef
):
    """
    Type definition for `ClientListResolversByFunctionResponseresolvers` `pipelineConfig`

    The ``PipelineConfig`` .

    - **functions** *(list) --*

      A list of ``Function`` objects.

      - *(string) --*
    """


_ClientListResolversByFunctionResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef = TypedDict(
    "_ClientListResolversByFunctionResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef",
    {"lambdaConflictHandlerArn": str},
    total=False,
)


class ClientListResolversByFunctionResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef(
    _ClientListResolversByFunctionResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef
):
    """
    Type definition for `ClientListResolversByFunctionResponseresolverssyncConfig`
    `lambdaConflictHandlerConfig`

    The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

    - **lambdaConflictHandlerArn** *(string) --*

      The Arn for the Lambda function to use as the Conflict Handler.
    """


_ClientListResolversByFunctionResponseresolverssyncConfigTypeDef = TypedDict(
    "_ClientListResolversByFunctionResponseresolverssyncConfigTypeDef",
    {
        "conflictHandler": str,
        "conflictDetection": str,
        "lambdaConflictHandlerConfig": ClientListResolversByFunctionResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef,
    },
    total=False,
)


class ClientListResolversByFunctionResponseresolverssyncConfigTypeDef(
    _ClientListResolversByFunctionResponseresolverssyncConfigTypeDef
):
    """
    Type definition for `ClientListResolversByFunctionResponseresolvers` `syncConfig`

    The ``SyncConfig`` for a resolver attached to a versioned datasource.

    - **conflictHandler** *(string) --*

      The Conflict Resolution strategy to perform in the event of a conflict.

      * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do not
      match the latest version at the server.

      * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

      * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
      LambdaConflictHandlerConfig.

    - **conflictDetection** *(string) --*

      The Conflict Detection strategy to use.

      * **VERSION** : Detect conflicts based on object versions for this resolver.

      * **NONE** : Do not detect conflicts when executing this resolver.

    - **lambdaConflictHandlerConfig** *(dict) --*

      The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

      - **lambdaConflictHandlerArn** *(string) --*

        The Arn for the Lambda function to use as the Conflict Handler.
    """


_ClientListResolversByFunctionResponseresolversTypeDef = TypedDict(
    "_ClientListResolversByFunctionResponseresolversTypeDef",
    {
        "typeName": str,
        "fieldName": str,
        "dataSourceName": str,
        "resolverArn": str,
        "requestMappingTemplate": str,
        "responseMappingTemplate": str,
        "kind": str,
        "pipelineConfig": ClientListResolversByFunctionResponseresolverspipelineConfigTypeDef,
        "syncConfig": ClientListResolversByFunctionResponseresolverssyncConfigTypeDef,
        "cachingConfig": ClientListResolversByFunctionResponseresolverscachingConfigTypeDef,
    },
    total=False,
)


class ClientListResolversByFunctionResponseresolversTypeDef(
    _ClientListResolversByFunctionResponseresolversTypeDef
):
    """
    Type definition for `ClientListResolversByFunctionResponse` `resolvers`

    Describes a resolver.

    - **typeName** *(string) --*

      The resolver type name.

    - **fieldName** *(string) --*

      The resolver field name.

    - **dataSourceName** *(string) --*

      The resolver data source name.

    - **resolverArn** *(string) --*

      The resolver ARN.

    - **requestMappingTemplate** *(string) --*

      The request mapping template.

    - **responseMappingTemplate** *(string) --*

      The response mapping template.

    - **kind** *(string) --*

      The resolver type.

      * **UNIT** : A UNIT resolver type. A UNIT resolver is the default resolver type. A UNIT
      resolver enables you to execute a GraphQL query against a single data source.

      * **PIPELINE** : A PIPELINE resolver type. A PIPELINE resolver enables you to execute a series
      of ``Function`` in a serial manner. You can use a pipeline resolver to execute a GraphQL query
      against multiple data sources.

    - **pipelineConfig** *(dict) --*

      The ``PipelineConfig`` .

      - **functions** *(list) --*

        A list of ``Function`` objects.

        - *(string) --*

    - **syncConfig** *(dict) --*

      The ``SyncConfig`` for a resolver attached to a versioned datasource.

      - **conflictHandler** *(string) --*

        The Conflict Resolution strategy to perform in the event of a conflict.

        * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do not
        match the latest version at the server.

        * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

        * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
        LambdaConflictHandlerConfig.

      - **conflictDetection** *(string) --*

        The Conflict Detection strategy to use.

        * **VERSION** : Detect conflicts based on object versions for this resolver.

        * **NONE** : Do not detect conflicts when executing this resolver.

      - **lambdaConflictHandlerConfig** *(dict) --*

        The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

        - **lambdaConflictHandlerArn** *(string) --*

          The Arn for the Lambda function to use as the Conflict Handler.

    - **cachingConfig** *(dict) --*

      The caching configuration for the resolver.

      - **ttl** *(integer) --*

        The TTL in seconds for a resolver that has caching enabled.

        Valid values are between 1 and 3600 seconds.

      - **cachingKeys** *(list) --*

        The caching keys for a resolver that has caching enabled.

        Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

        - *(string) --*
    """


_ClientListResolversByFunctionResponseTypeDef = TypedDict(
    "_ClientListResolversByFunctionResponseTypeDef",
    {"resolvers": List[ClientListResolversByFunctionResponseresolversTypeDef], "nextToken": str},
    total=False,
)


class ClientListResolversByFunctionResponseTypeDef(_ClientListResolversByFunctionResponseTypeDef):
    """
    Type definition for `ClientListResolversByFunction` `Response`

    - **resolvers** *(list) --*

      The list of resolvers.

      - *(dict) --*

        Describes a resolver.

        - **typeName** *(string) --*

          The resolver type name.

        - **fieldName** *(string) --*

          The resolver field name.

        - **dataSourceName** *(string) --*

          The resolver data source name.

        - **resolverArn** *(string) --*

          The resolver ARN.

        - **requestMappingTemplate** *(string) --*

          The request mapping template.

        - **responseMappingTemplate** *(string) --*

          The response mapping template.

        - **kind** *(string) --*

          The resolver type.

          * **UNIT** : A UNIT resolver type. A UNIT resolver is the default resolver type. A UNIT
          resolver enables you to execute a GraphQL query against a single data source.

          * **PIPELINE** : A PIPELINE resolver type. A PIPELINE resolver enables you to execute a
          series of ``Function`` in a serial manner. You can use a pipeline resolver to execute a
          GraphQL query against multiple data sources.

        - **pipelineConfig** *(dict) --*

          The ``PipelineConfig`` .

          - **functions** *(list) --*

            A list of ``Function`` objects.

            - *(string) --*

        - **syncConfig** *(dict) --*

          The ``SyncConfig`` for a resolver attached to a versioned datasource.

          - **conflictHandler** *(string) --*

            The Conflict Resolution strategy to perform in the event of a conflict.

            * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do
            not match the latest version at the server.

            * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

            * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
            LambdaConflictHandlerConfig.

          - **conflictDetection** *(string) --*

            The Conflict Detection strategy to use.

            * **VERSION** : Detect conflicts based on object versions for this resolver.

            * **NONE** : Do not detect conflicts when executing this resolver.

          - **lambdaConflictHandlerConfig** *(dict) --*

            The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

            - **lambdaConflictHandlerArn** *(string) --*

              The Arn for the Lambda function to use as the Conflict Handler.

        - **cachingConfig** *(dict) --*

          The caching configuration for the resolver.

          - **ttl** *(integer) --*

            The TTL in seconds for a resolver that has caching enabled.

            Valid values are between 1 and 3600 seconds.

          - **cachingKeys** *(list) --*

            The caching keys for a resolver that has caching enabled.

            Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

            - *(string) --*

    - **nextToken** *(string) --*

      An identifier that can be used to return the next set of items in the list.
    """


_ClientListResolversResponseresolverscachingConfigTypeDef = TypedDict(
    "_ClientListResolversResponseresolverscachingConfigTypeDef",
    {"ttl": int, "cachingKeys": List[str]},
    total=False,
)


class ClientListResolversResponseresolverscachingConfigTypeDef(
    _ClientListResolversResponseresolverscachingConfigTypeDef
):
    """
    Type definition for `ClientListResolversResponseresolvers` `cachingConfig`

    The caching configuration for the resolver.

    - **ttl** *(integer) --*

      The TTL in seconds for a resolver that has caching enabled.

      Valid values are between 1 and 3600 seconds.

    - **cachingKeys** *(list) --*

      The caching keys for a resolver that has caching enabled.

      Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

      - *(string) --*
    """


_ClientListResolversResponseresolverspipelineConfigTypeDef = TypedDict(
    "_ClientListResolversResponseresolverspipelineConfigTypeDef",
    {"functions": List[str]},
    total=False,
)


class ClientListResolversResponseresolverspipelineConfigTypeDef(
    _ClientListResolversResponseresolverspipelineConfigTypeDef
):
    """
    Type definition for `ClientListResolversResponseresolvers` `pipelineConfig`

    The ``PipelineConfig`` .

    - **functions** *(list) --*

      A list of ``Function`` objects.

      - *(string) --*
    """


_ClientListResolversResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef = TypedDict(
    "_ClientListResolversResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef",
    {"lambdaConflictHandlerArn": str},
    total=False,
)


class ClientListResolversResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef(
    _ClientListResolversResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef
):
    """
    Type definition for `ClientListResolversResponseresolverssyncConfig`
    `lambdaConflictHandlerConfig`

    The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

    - **lambdaConflictHandlerArn** *(string) --*

      The Arn for the Lambda function to use as the Conflict Handler.
    """


_ClientListResolversResponseresolverssyncConfigTypeDef = TypedDict(
    "_ClientListResolversResponseresolverssyncConfigTypeDef",
    {
        "conflictHandler": str,
        "conflictDetection": str,
        "lambdaConflictHandlerConfig": ClientListResolversResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef,
    },
    total=False,
)


class ClientListResolversResponseresolverssyncConfigTypeDef(
    _ClientListResolversResponseresolverssyncConfigTypeDef
):
    """
    Type definition for `ClientListResolversResponseresolvers` `syncConfig`

    The ``SyncConfig`` for a resolver attached to a versioned datasource.

    - **conflictHandler** *(string) --*

      The Conflict Resolution strategy to perform in the event of a conflict.

      * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do not
      match the latest version at the server.

      * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

      * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
      LambdaConflictHandlerConfig.

    - **conflictDetection** *(string) --*

      The Conflict Detection strategy to use.

      * **VERSION** : Detect conflicts based on object versions for this resolver.

      * **NONE** : Do not detect conflicts when executing this resolver.

    - **lambdaConflictHandlerConfig** *(dict) --*

      The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

      - **lambdaConflictHandlerArn** *(string) --*

        The Arn for the Lambda function to use as the Conflict Handler.
    """


_ClientListResolversResponseresolversTypeDef = TypedDict(
    "_ClientListResolversResponseresolversTypeDef",
    {
        "typeName": str,
        "fieldName": str,
        "dataSourceName": str,
        "resolverArn": str,
        "requestMappingTemplate": str,
        "responseMappingTemplate": str,
        "kind": str,
        "pipelineConfig": ClientListResolversResponseresolverspipelineConfigTypeDef,
        "syncConfig": ClientListResolversResponseresolverssyncConfigTypeDef,
        "cachingConfig": ClientListResolversResponseresolverscachingConfigTypeDef,
    },
    total=False,
)


class ClientListResolversResponseresolversTypeDef(_ClientListResolversResponseresolversTypeDef):
    """
    Type definition for `ClientListResolversResponse` `resolvers`

    Describes a resolver.

    - **typeName** *(string) --*

      The resolver type name.

    - **fieldName** *(string) --*

      The resolver field name.

    - **dataSourceName** *(string) --*

      The resolver data source name.

    - **resolverArn** *(string) --*

      The resolver ARN.

    - **requestMappingTemplate** *(string) --*

      The request mapping template.

    - **responseMappingTemplate** *(string) --*

      The response mapping template.

    - **kind** *(string) --*

      The resolver type.

      * **UNIT** : A UNIT resolver type. A UNIT resolver is the default resolver type. A UNIT
      resolver enables you to execute a GraphQL query against a single data source.

      * **PIPELINE** : A PIPELINE resolver type. A PIPELINE resolver enables you to execute a series
      of ``Function`` in a serial manner. You can use a pipeline resolver to execute a GraphQL query
      against multiple data sources.

    - **pipelineConfig** *(dict) --*

      The ``PipelineConfig`` .

      - **functions** *(list) --*

        A list of ``Function`` objects.

        - *(string) --*

    - **syncConfig** *(dict) --*

      The ``SyncConfig`` for a resolver attached to a versioned datasource.

      - **conflictHandler** *(string) --*

        The Conflict Resolution strategy to perform in the event of a conflict.

        * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do not
        match the latest version at the server.

        * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

        * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
        LambdaConflictHandlerConfig.

      - **conflictDetection** *(string) --*

        The Conflict Detection strategy to use.

        * **VERSION** : Detect conflicts based on object versions for this resolver.

        * **NONE** : Do not detect conflicts when executing this resolver.

      - **lambdaConflictHandlerConfig** *(dict) --*

        The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

        - **lambdaConflictHandlerArn** *(string) --*

          The Arn for the Lambda function to use as the Conflict Handler.

    - **cachingConfig** *(dict) --*

      The caching configuration for the resolver.

      - **ttl** *(integer) --*

        The TTL in seconds for a resolver that has caching enabled.

        Valid values are between 1 and 3600 seconds.

      - **cachingKeys** *(list) --*

        The caching keys for a resolver that has caching enabled.

        Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

        - *(string) --*
    """


_ClientListResolversResponseTypeDef = TypedDict(
    "_ClientListResolversResponseTypeDef",
    {"resolvers": List[ClientListResolversResponseresolversTypeDef], "nextToken": str},
    total=False,
)


class ClientListResolversResponseTypeDef(_ClientListResolversResponseTypeDef):
    """
    Type definition for `ClientListResolvers` `Response`

    - **resolvers** *(list) --*

      The ``Resolver`` objects.

      - *(dict) --*

        Describes a resolver.

        - **typeName** *(string) --*

          The resolver type name.

        - **fieldName** *(string) --*

          The resolver field name.

        - **dataSourceName** *(string) --*

          The resolver data source name.

        - **resolverArn** *(string) --*

          The resolver ARN.

        - **requestMappingTemplate** *(string) --*

          The request mapping template.

        - **responseMappingTemplate** *(string) --*

          The response mapping template.

        - **kind** *(string) --*

          The resolver type.

          * **UNIT** : A UNIT resolver type. A UNIT resolver is the default resolver type. A UNIT
          resolver enables you to execute a GraphQL query against a single data source.

          * **PIPELINE** : A PIPELINE resolver type. A PIPELINE resolver enables you to execute a
          series of ``Function`` in a serial manner. You can use a pipeline resolver to execute a
          GraphQL query against multiple data sources.

        - **pipelineConfig** *(dict) --*

          The ``PipelineConfig`` .

          - **functions** *(list) --*

            A list of ``Function`` objects.

            - *(string) --*

        - **syncConfig** *(dict) --*

          The ``SyncConfig`` for a resolver attached to a versioned datasource.

          - **conflictHandler** *(string) --*

            The Conflict Resolution strategy to perform in the event of a conflict.

            * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do
            not match the latest version at the server.

            * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

            * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
            LambdaConflictHandlerConfig.

          - **conflictDetection** *(string) --*

            The Conflict Detection strategy to use.

            * **VERSION** : Detect conflicts based on object versions for this resolver.

            * **NONE** : Do not detect conflicts when executing this resolver.

          - **lambdaConflictHandlerConfig** *(dict) --*

            The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

            - **lambdaConflictHandlerArn** *(string) --*

              The Arn for the Lambda function to use as the Conflict Handler.

        - **cachingConfig** *(dict) --*

          The caching configuration for the resolver.

          - **ttl** *(integer) --*

            The TTL in seconds for a resolver that has caching enabled.

            Valid values are between 1 and 3600 seconds.

          - **cachingKeys** *(list) --*

            The caching keys for a resolver that has caching enabled.

            Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

            - *(string) --*

    - **nextToken** *(string) --*

      An identifier to be passed in the next request to this operation to return the next set of
      items in the list.
    """


_ClientListTagsForResourceResponseTypeDef = TypedDict(
    "_ClientListTagsForResourceResponseTypeDef", {"tags": Dict[str, str]}, total=False
)


class ClientListTagsForResourceResponseTypeDef(_ClientListTagsForResourceResponseTypeDef):
    """
    Type definition for `ClientListTagsForResource` `Response`

    - **tags** *(dict) --*

      A ``TagMap`` object.

      - *(string) --*

        The key for the tag.

        - *(string) --*

          The value for the tag.
    """


_ClientListTypesResponsetypesTypeDef = TypedDict(
    "_ClientListTypesResponsetypesTypeDef",
    {"name": str, "description": str, "arn": str, "definition": str, "format": str},
    total=False,
)


class ClientListTypesResponsetypesTypeDef(_ClientListTypesResponsetypesTypeDef):
    """
    Type definition for `ClientListTypesResponse` `types`

    Describes a type.

    - **name** *(string) --*

      The type name.

    - **description** *(string) --*

      The type description.

    - **arn** *(string) --*

      The type ARN.

    - **definition** *(string) --*

      The type definition.

    - **format** *(string) --*

      The type format: SDL or JSON.
    """


_ClientListTypesResponseTypeDef = TypedDict(
    "_ClientListTypesResponseTypeDef",
    {"types": List[ClientListTypesResponsetypesTypeDef], "nextToken": str},
    total=False,
)


class ClientListTypesResponseTypeDef(_ClientListTypesResponseTypeDef):
    """
    Type definition for `ClientListTypes` `Response`

    - **types** *(list) --*

      The ``Type`` objects.

      - *(dict) --*

        Describes a type.

        - **name** *(string) --*

          The type name.

        - **description** *(string) --*

          The type description.

        - **arn** *(string) --*

          The type ARN.

        - **definition** *(string) --*

          The type definition.

        - **format** *(string) --*

          The type format: SDL or JSON.

    - **nextToken** *(string) --*

      An identifier to be passed in the next request to this operation to return the next set of
      items in the list.
    """


_ClientStartSchemaCreationResponseTypeDef = TypedDict(
    "_ClientStartSchemaCreationResponseTypeDef", {"status": str}, total=False
)


class ClientStartSchemaCreationResponseTypeDef(_ClientStartSchemaCreationResponseTypeDef):
    """
    Type definition for `ClientStartSchemaCreation` `Response`

    - **status** *(string) --*

      The current state of the schema (PROCESSING, FAILED, SUCCESS, or NOT_APPLICABLE). When the
      schema is in the ACTIVE state, you can add data.
    """


_ClientUpdateApiCacheResponseapiCacheTypeDef = TypedDict(
    "_ClientUpdateApiCacheResponseapiCacheTypeDef",
    {
        "ttl": int,
        "apiCachingBehavior": str,
        "transitEncryptionEnabled": bool,
        "atRestEncryptionEnabled": bool,
        "type": str,
        "status": str,
    },
    total=False,
)


class ClientUpdateApiCacheResponseapiCacheTypeDef(_ClientUpdateApiCacheResponseapiCacheTypeDef):
    """
    Type definition for `ClientUpdateApiCacheResponse` `apiCache`

    The ``ApiCache`` object.

    - **ttl** *(integer) --*

      TTL in seconds for cache entries.

      Valid values are between 1 and 3600 seconds.

    - **apiCachingBehavior** *(string) --*

      Caching behavior.

      * **FULL_REQUEST_CACHING** : All requests are fully cached.

      * **PER_RESOLVER_CACHING** : Individual resovlers that you specify are cached.

    - **transitEncryptionEnabled** *(boolean) --*

      Transit encryption flag when connecting to cache. This setting cannot be updated after
      creation.

    - **atRestEncryptionEnabled** *(boolean) --*

      At rest encryption flag for cache. This setting cannot be updated after creation.

    - **type** *(string) --*

      The cache instance type.

      * **T2_SMALL** : A t2.small instance type.

      * **T2_MEDIUM** : A t2.medium instance type.

      * **R4_LARGE** : A r4.large instance type.

      * **R4_XLARGE** : A r4.xlarge instance type.

      * **R4_2XLARGE** : A r4.2xlarge instance type.

      * **R4_4XLARGE** : A r4.4xlarge instance type.

      * **R4_8XLARGE** : A r4.8xlarge instance type.

    - **status** *(string) --*

      The cache instance status.

      * **AVAILABLE** : The instance is available for use.

      * **CREATING** : The instance is currently creating.

      * **DELETING** : The instance is currently deleting.

      * **MODIFYING** : The instance is currently modifying.

      * **FAILED** : The instance has failed creation.
    """


_ClientUpdateApiCacheResponseTypeDef = TypedDict(
    "_ClientUpdateApiCacheResponseTypeDef",
    {"apiCache": ClientUpdateApiCacheResponseapiCacheTypeDef},
    total=False,
)


class ClientUpdateApiCacheResponseTypeDef(_ClientUpdateApiCacheResponseTypeDef):
    """
    Type definition for `ClientUpdateApiCache` `Response`

    Represents the output of a ``UpdateApiCache`` operation.

    - **apiCache** *(dict) --*

      The ``ApiCache`` object.

      - **ttl** *(integer) --*

        TTL in seconds for cache entries.

        Valid values are between 1 and 3600 seconds.

      - **apiCachingBehavior** *(string) --*

        Caching behavior.

        * **FULL_REQUEST_CACHING** : All requests are fully cached.

        * **PER_RESOLVER_CACHING** : Individual resovlers that you specify are cached.

      - **transitEncryptionEnabled** *(boolean) --*

        Transit encryption flag when connecting to cache. This setting cannot be updated after
        creation.

      - **atRestEncryptionEnabled** *(boolean) --*

        At rest encryption flag for cache. This setting cannot be updated after creation.

      - **type** *(string) --*

        The cache instance type.

        * **T2_SMALL** : A t2.small instance type.

        * **T2_MEDIUM** : A t2.medium instance type.

        * **R4_LARGE** : A r4.large instance type.

        * **R4_XLARGE** : A r4.xlarge instance type.

        * **R4_2XLARGE** : A r4.2xlarge instance type.

        * **R4_4XLARGE** : A r4.4xlarge instance type.

        * **R4_8XLARGE** : A r4.8xlarge instance type.

      - **status** *(string) --*

        The cache instance status.

        * **AVAILABLE** : The instance is available for use.

        * **CREATING** : The instance is currently creating.

        * **DELETING** : The instance is currently deleting.

        * **MODIFYING** : The instance is currently modifying.

        * **FAILED** : The instance has failed creation.
    """


_ClientUpdateApiKeyResponseapiKeyTypeDef = TypedDict(
    "_ClientUpdateApiKeyResponseapiKeyTypeDef",
    {"id": str, "description": str, "expires": int},
    total=False,
)


class ClientUpdateApiKeyResponseapiKeyTypeDef(_ClientUpdateApiKeyResponseapiKeyTypeDef):
    """
    Type definition for `ClientUpdateApiKeyResponse` `apiKey`

    The API key.

    - **id** *(string) --*

      The API key ID.

    - **description** *(string) --*

      A description of the purpose of the API key.

    - **expires** *(integer) --*

      The time after which the API key expires. The date is represented as seconds since the epoch,
      rounded down to the nearest hour.
    """


_ClientUpdateApiKeyResponseTypeDef = TypedDict(
    "_ClientUpdateApiKeyResponseTypeDef",
    {"apiKey": ClientUpdateApiKeyResponseapiKeyTypeDef},
    total=False,
)


class ClientUpdateApiKeyResponseTypeDef(_ClientUpdateApiKeyResponseTypeDef):
    """
    Type definition for `ClientUpdateApiKey` `Response`

    - **apiKey** *(dict) --*

      The API key.

      - **id** *(string) --*

        The API key ID.

      - **description** *(string) --*

        A description of the purpose of the API key.

      - **expires** *(integer) --*

        The time after which the API key expires. The date is represented as seconds since the
        epoch, rounded down to the nearest hour.
    """


_ClientUpdateDataSourceResponsedataSourcedynamodbConfigdeltaSyncConfigTypeDef = TypedDict(
    "_ClientUpdateDataSourceResponsedataSourcedynamodbConfigdeltaSyncConfigTypeDef",
    {"baseTableTTL": int, "deltaSyncTableName": str, "deltaSyncTableTTL": int},
    total=False,
)


class ClientUpdateDataSourceResponsedataSourcedynamodbConfigdeltaSyncConfigTypeDef(
    _ClientUpdateDataSourceResponsedataSourcedynamodbConfigdeltaSyncConfigTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceResponsedataSourcedynamodbConfig` `deltaSyncConfig`

    The ``DeltaSyncConfig`` for a versioned datasource.

    - **baseTableTTL** *(integer) --*

      The number of minutes an Item is stored in the datasource.

    - **deltaSyncTableName** *(string) --*

      The Delta Sync table name.

    - **deltaSyncTableTTL** *(integer) --*

      The number of minutes a Delta Sync log entry is stored in the Delta Sync table.
    """


_ClientUpdateDataSourceResponsedataSourcedynamodbConfigTypeDef = TypedDict(
    "_ClientUpdateDataSourceResponsedataSourcedynamodbConfigTypeDef",
    {
        "tableName": str,
        "awsRegion": str,
        "useCallerCredentials": bool,
        "deltaSyncConfig": ClientUpdateDataSourceResponsedataSourcedynamodbConfigdeltaSyncConfigTypeDef,
        "versioned": bool,
    },
    total=False,
)


class ClientUpdateDataSourceResponsedataSourcedynamodbConfigTypeDef(
    _ClientUpdateDataSourceResponsedataSourcedynamodbConfigTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceResponsedataSource` `dynamodbConfig`

    Amazon DynamoDB settings.

    - **tableName** *(string) --*

      The table name.

    - **awsRegion** *(string) --*

      The AWS Region.

    - **useCallerCredentials** *(boolean) --*

      Set to TRUE to use Amazon Cognito credentials with this data source.

    - **deltaSyncConfig** *(dict) --*

      The ``DeltaSyncConfig`` for a versioned datasource.

      - **baseTableTTL** *(integer) --*

        The number of minutes an Item is stored in the datasource.

      - **deltaSyncTableName** *(string) --*

        The Delta Sync table name.

      - **deltaSyncTableTTL** *(integer) --*

        The number of minutes a Delta Sync log entry is stored in the Delta Sync table.

    - **versioned** *(boolean) --*

      Set to TRUE to use Conflict Detection and Resolution with this data source.
    """


_ClientUpdateDataSourceResponsedataSourceelasticsearchConfigTypeDef = TypedDict(
    "_ClientUpdateDataSourceResponsedataSourceelasticsearchConfigTypeDef",
    {"endpoint": str, "awsRegion": str},
    total=False,
)


class ClientUpdateDataSourceResponsedataSourceelasticsearchConfigTypeDef(
    _ClientUpdateDataSourceResponsedataSourceelasticsearchConfigTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceResponsedataSource` `elasticsearchConfig`

    Amazon Elasticsearch Service settings.

    - **endpoint** *(string) --*

      The endpoint.

    - **awsRegion** *(string) --*

      The AWS Region.
    """


_ClientUpdateDataSourceResponsedataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef = TypedDict(
    "_ClientUpdateDataSourceResponsedataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef",
    {"signingRegion": str, "signingServiceName": str},
    total=False,
)


class ClientUpdateDataSourceResponsedataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef(
    _ClientUpdateDataSourceResponsedataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceResponsedataSourcehttpConfigauthorizationConfig`
    `awsIamConfig`

    The AWS IAM settings.

    - **signingRegion** *(string) --*

      The signing region for AWS IAM authorization.

    - **signingServiceName** *(string) --*

      The signing service name for AWS IAM authorization.
    """


_ClientUpdateDataSourceResponsedataSourcehttpConfigauthorizationConfigTypeDef = TypedDict(
    "_ClientUpdateDataSourceResponsedataSourcehttpConfigauthorizationConfigTypeDef",
    {
        "authorizationType": str,
        "awsIamConfig": ClientUpdateDataSourceResponsedataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef,
    },
    total=False,
)


class ClientUpdateDataSourceResponsedataSourcehttpConfigauthorizationConfigTypeDef(
    _ClientUpdateDataSourceResponsedataSourcehttpConfigauthorizationConfigTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceResponsedataSourcehttpConfig` `authorizationConfig`

    The authorization config in case the HTTP endpoint requires authorization.

    - **authorizationType** *(string) --*

      The authorization type required by the HTTP endpoint.

      * **AWS_IAM** : The authorization type is Sigv4.

    - **awsIamConfig** *(dict) --*

      The AWS IAM settings.

      - **signingRegion** *(string) --*

        The signing region for AWS IAM authorization.

      - **signingServiceName** *(string) --*

        The signing service name for AWS IAM authorization.
    """


_ClientUpdateDataSourceResponsedataSourcehttpConfigTypeDef = TypedDict(
    "_ClientUpdateDataSourceResponsedataSourcehttpConfigTypeDef",
    {
        "endpoint": str,
        "authorizationConfig": ClientUpdateDataSourceResponsedataSourcehttpConfigauthorizationConfigTypeDef,
    },
    total=False,
)


class ClientUpdateDataSourceResponsedataSourcehttpConfigTypeDef(
    _ClientUpdateDataSourceResponsedataSourcehttpConfigTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceResponsedataSource` `httpConfig`

    HTTP endpoint settings.

    - **endpoint** *(string) --*

      The HTTP URL endpoint. You can either specify the domain name or IP, and port combination, and
      the URL scheme must be HTTP or HTTPS. If the port is not specified, AWS AppSync uses the
      default port 80 for the HTTP endpoint and port 443 for HTTPS endpoints.

    - **authorizationConfig** *(dict) --*

      The authorization config in case the HTTP endpoint requires authorization.

      - **authorizationType** *(string) --*

        The authorization type required by the HTTP endpoint.

        * **AWS_IAM** : The authorization type is Sigv4.

      - **awsIamConfig** *(dict) --*

        The AWS IAM settings.

        - **signingRegion** *(string) --*

          The signing region for AWS IAM authorization.

        - **signingServiceName** *(string) --*

          The signing service name for AWS IAM authorization.
    """


_ClientUpdateDataSourceResponsedataSourcelambdaConfigTypeDef = TypedDict(
    "_ClientUpdateDataSourceResponsedataSourcelambdaConfigTypeDef",
    {"lambdaFunctionArn": str},
    total=False,
)


class ClientUpdateDataSourceResponsedataSourcelambdaConfigTypeDef(
    _ClientUpdateDataSourceResponsedataSourcelambdaConfigTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceResponsedataSource` `lambdaConfig`

    AWS Lambda settings.

    - **lambdaFunctionArn** *(string) --*

      The ARN for the Lambda function.
    """


_ClientUpdateDataSourceResponsedataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef = TypedDict(
    "_ClientUpdateDataSourceResponsedataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef",
    {
        "awsRegion": str,
        "dbClusterIdentifier": str,
        "databaseName": str,
        "schema": str,
        "awsSecretStoreArn": str,
    },
    total=False,
)


class ClientUpdateDataSourceResponsedataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef(
    _ClientUpdateDataSourceResponsedataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceResponsedataSourcerelationalDatabaseConfig`
    `rdsHttpEndpointConfig`

    Amazon RDS HTTP endpoint settings.

    - **awsRegion** *(string) --*

      AWS Region for RDS HTTP endpoint.

    - **dbClusterIdentifier** *(string) --*

      Amazon RDS cluster identifier.

    - **databaseName** *(string) --*

      Logical database name.

    - **schema** *(string) --*

      Logical schema name.

    - **awsSecretStoreArn** *(string) --*

      AWS secret store ARN for database credentials.
    """


_ClientUpdateDataSourceResponsedataSourcerelationalDatabaseConfigTypeDef = TypedDict(
    "_ClientUpdateDataSourceResponsedataSourcerelationalDatabaseConfigTypeDef",
    {
        "relationalDatabaseSourceType": str,
        "rdsHttpEndpointConfig": ClientUpdateDataSourceResponsedataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef,
    },
    total=False,
)


class ClientUpdateDataSourceResponsedataSourcerelationalDatabaseConfigTypeDef(
    _ClientUpdateDataSourceResponsedataSourcerelationalDatabaseConfigTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceResponsedataSource` `relationalDatabaseConfig`

    Relational database settings.

    - **relationalDatabaseSourceType** *(string) --*

      Source type for the relational database.

      * **RDS_HTTP_ENDPOINT** : The relational database source type is an Amazon RDS HTTP endpoint.

    - **rdsHttpEndpointConfig** *(dict) --*

      Amazon RDS HTTP endpoint settings.

      - **awsRegion** *(string) --*

        AWS Region for RDS HTTP endpoint.

      - **dbClusterIdentifier** *(string) --*

        Amazon RDS cluster identifier.

      - **databaseName** *(string) --*

        Logical database name.

      - **schema** *(string) --*

        Logical schema name.

      - **awsSecretStoreArn** *(string) --*

        AWS secret store ARN for database credentials.
    """


_ClientUpdateDataSourceResponsedataSourceTypeDef = TypedDict(
    "_ClientUpdateDataSourceResponsedataSourceTypeDef",
    {
        "dataSourceArn": str,
        "name": str,
        "description": str,
        "type": str,
        "serviceRoleArn": str,
        "dynamodbConfig": ClientUpdateDataSourceResponsedataSourcedynamodbConfigTypeDef,
        "lambdaConfig": ClientUpdateDataSourceResponsedataSourcelambdaConfigTypeDef,
        "elasticsearchConfig": ClientUpdateDataSourceResponsedataSourceelasticsearchConfigTypeDef,
        "httpConfig": ClientUpdateDataSourceResponsedataSourcehttpConfigTypeDef,
        "relationalDatabaseConfig": ClientUpdateDataSourceResponsedataSourcerelationalDatabaseConfigTypeDef,
    },
    total=False,
)


class ClientUpdateDataSourceResponsedataSourceTypeDef(
    _ClientUpdateDataSourceResponsedataSourceTypeDef
):
    """
    Type definition for `ClientUpdateDataSourceResponse` `dataSource`

    The updated ``DataSource`` object.

    - **dataSourceArn** *(string) --*

      The data source ARN.

    - **name** *(string) --*

      The name of the data source.

    - **description** *(string) --*

      The description of the data source.

    - **type** *(string) --*

      The type of the data source.

      * **AMAZON_DYNAMODB** : The data source is an Amazon DynamoDB table.

      * **AMAZON_ELASTICSEARCH** : The data source is an Amazon Elasticsearch Service domain.

      * **AWS_LAMBDA** : The data source is an AWS Lambda function.

      * **NONE** : There is no data source. This type is used when you wish to invoke a GraphQL
      operation without connecting to a data source, such as performing data transformation with
      resolvers or triggering a subscription to be invoked from a mutation.

      * **HTTP** : The data source is an HTTP endpoint.

      * **RELATIONAL_DATABASE** : The data source is a relational database.

    - **serviceRoleArn** *(string) --*

      The AWS IAM service role ARN for the data source. The system assumes this role when accessing
      the data source.

    - **dynamodbConfig** *(dict) --*

      Amazon DynamoDB settings.

      - **tableName** *(string) --*

        The table name.

      - **awsRegion** *(string) --*

        The AWS Region.

      - **useCallerCredentials** *(boolean) --*

        Set to TRUE to use Amazon Cognito credentials with this data source.

      - **deltaSyncConfig** *(dict) --*

        The ``DeltaSyncConfig`` for a versioned datasource.

        - **baseTableTTL** *(integer) --*

          The number of minutes an Item is stored in the datasource.

        - **deltaSyncTableName** *(string) --*

          The Delta Sync table name.

        - **deltaSyncTableTTL** *(integer) --*

          The number of minutes a Delta Sync log entry is stored in the Delta Sync table.

      - **versioned** *(boolean) --*

        Set to TRUE to use Conflict Detection and Resolution with this data source.

    - **lambdaConfig** *(dict) --*

      AWS Lambda settings.

      - **lambdaFunctionArn** *(string) --*

        The ARN for the Lambda function.

    - **elasticsearchConfig** *(dict) --*

      Amazon Elasticsearch Service settings.

      - **endpoint** *(string) --*

        The endpoint.

      - **awsRegion** *(string) --*

        The AWS Region.

    - **httpConfig** *(dict) --*

      HTTP endpoint settings.

      - **endpoint** *(string) --*

        The HTTP URL endpoint. You can either specify the domain name or IP, and port combination,
        and the URL scheme must be HTTP or HTTPS. If the port is not specified, AWS AppSync uses the
        default port 80 for the HTTP endpoint and port 443 for HTTPS endpoints.

      - **authorizationConfig** *(dict) --*

        The authorization config in case the HTTP endpoint requires authorization.

        - **authorizationType** *(string) --*

          The authorization type required by the HTTP endpoint.

          * **AWS_IAM** : The authorization type is Sigv4.

        - **awsIamConfig** *(dict) --*

          The AWS IAM settings.

          - **signingRegion** *(string) --*

            The signing region for AWS IAM authorization.

          - **signingServiceName** *(string) --*

            The signing service name for AWS IAM authorization.

    - **relationalDatabaseConfig** *(dict) --*

      Relational database settings.

      - **relationalDatabaseSourceType** *(string) --*

        Source type for the relational database.

        * **RDS_HTTP_ENDPOINT** : The relational database source type is an Amazon RDS HTTP
        endpoint.

      - **rdsHttpEndpointConfig** *(dict) --*

        Amazon RDS HTTP endpoint settings.

        - **awsRegion** *(string) --*

          AWS Region for RDS HTTP endpoint.

        - **dbClusterIdentifier** *(string) --*

          Amazon RDS cluster identifier.

        - **databaseName** *(string) --*

          Logical database name.

        - **schema** *(string) --*

          Logical schema name.

        - **awsSecretStoreArn** *(string) --*

          AWS secret store ARN for database credentials.
    """


_ClientUpdateDataSourceResponseTypeDef = TypedDict(
    "_ClientUpdateDataSourceResponseTypeDef",
    {"dataSource": ClientUpdateDataSourceResponsedataSourceTypeDef},
    total=False,
)


class ClientUpdateDataSourceResponseTypeDef(_ClientUpdateDataSourceResponseTypeDef):
    """
    Type definition for `ClientUpdateDataSource` `Response`

    - **dataSource** *(dict) --*

      The updated ``DataSource`` object.

      - **dataSourceArn** *(string) --*

        The data source ARN.

      - **name** *(string) --*

        The name of the data source.

      - **description** *(string) --*

        The description of the data source.

      - **type** *(string) --*

        The type of the data source.

        * **AMAZON_DYNAMODB** : The data source is an Amazon DynamoDB table.

        * **AMAZON_ELASTICSEARCH** : The data source is an Amazon Elasticsearch Service domain.

        * **AWS_LAMBDA** : The data source is an AWS Lambda function.

        * **NONE** : There is no data source. This type is used when you wish to invoke a GraphQL
        operation without connecting to a data source, such as performing data transformation with
        resolvers or triggering a subscription to be invoked from a mutation.

        * **HTTP** : The data source is an HTTP endpoint.

        * **RELATIONAL_DATABASE** : The data source is a relational database.

      - **serviceRoleArn** *(string) --*

        The AWS IAM service role ARN for the data source. The system assumes this role when
        accessing the data source.

      - **dynamodbConfig** *(dict) --*

        Amazon DynamoDB settings.

        - **tableName** *(string) --*

          The table name.

        - **awsRegion** *(string) --*

          The AWS Region.

        - **useCallerCredentials** *(boolean) --*

          Set to TRUE to use Amazon Cognito credentials with this data source.

        - **deltaSyncConfig** *(dict) --*

          The ``DeltaSyncConfig`` for a versioned datasource.

          - **baseTableTTL** *(integer) --*

            The number of minutes an Item is stored in the datasource.

          - **deltaSyncTableName** *(string) --*

            The Delta Sync table name.

          - **deltaSyncTableTTL** *(integer) --*

            The number of minutes a Delta Sync log entry is stored in the Delta Sync table.

        - **versioned** *(boolean) --*

          Set to TRUE to use Conflict Detection and Resolution with this data source.

      - **lambdaConfig** *(dict) --*

        AWS Lambda settings.

        - **lambdaFunctionArn** *(string) --*

          The ARN for the Lambda function.

      - **elasticsearchConfig** *(dict) --*

        Amazon Elasticsearch Service settings.

        - **endpoint** *(string) --*

          The endpoint.

        - **awsRegion** *(string) --*

          The AWS Region.

      - **httpConfig** *(dict) --*

        HTTP endpoint settings.

        - **endpoint** *(string) --*

          The HTTP URL endpoint. You can either specify the domain name or IP, and port combination,
          and the URL scheme must be HTTP or HTTPS. If the port is not specified, AWS AppSync uses
          the default port 80 for the HTTP endpoint and port 443 for HTTPS endpoints.

        - **authorizationConfig** *(dict) --*

          The authorization config in case the HTTP endpoint requires authorization.

          - **authorizationType** *(string) --*

            The authorization type required by the HTTP endpoint.

            * **AWS_IAM** : The authorization type is Sigv4.

          - **awsIamConfig** *(dict) --*

            The AWS IAM settings.

            - **signingRegion** *(string) --*

              The signing region for AWS IAM authorization.

            - **signingServiceName** *(string) --*

              The signing service name for AWS IAM authorization.

      - **relationalDatabaseConfig** *(dict) --*

        Relational database settings.

        - **relationalDatabaseSourceType** *(string) --*

          Source type for the relational database.

          * **RDS_HTTP_ENDPOINT** : The relational database source type is an Amazon RDS HTTP
          endpoint.

        - **rdsHttpEndpointConfig** *(dict) --*

          Amazon RDS HTTP endpoint settings.

          - **awsRegion** *(string) --*

            AWS Region for RDS HTTP endpoint.

          - **dbClusterIdentifier** *(string) --*

            Amazon RDS cluster identifier.

          - **databaseName** *(string) --*

            Logical database name.

          - **schema** *(string) --*

            Logical schema name.

          - **awsSecretStoreArn** *(string) --*

            AWS secret store ARN for database credentials.
    """


_ClientUpdateDataSourcedynamodbConfigdeltaSyncConfigTypeDef = TypedDict(
    "_ClientUpdateDataSourcedynamodbConfigdeltaSyncConfigTypeDef",
    {"baseTableTTL": int, "deltaSyncTableName": str, "deltaSyncTableTTL": int},
    total=False,
)


class ClientUpdateDataSourcedynamodbConfigdeltaSyncConfigTypeDef(
    _ClientUpdateDataSourcedynamodbConfigdeltaSyncConfigTypeDef
):
    """
    Type definition for `ClientUpdateDataSourcedynamodbConfig` `deltaSyncConfig`

    The ``DeltaSyncConfig`` for a versioned datasource.

    - **baseTableTTL** *(integer) --*

      The number of minutes an Item is stored in the datasource.

    - **deltaSyncTableName** *(string) --*

      The Delta Sync table name.

    - **deltaSyncTableTTL** *(integer) --*

      The number of minutes a Delta Sync log entry is stored in the Delta Sync table.
    """


_RequiredClientUpdateDataSourcedynamodbConfigTypeDef = TypedDict(
    "_RequiredClientUpdateDataSourcedynamodbConfigTypeDef", {"tableName": str, "awsRegion": str}
)
_OptionalClientUpdateDataSourcedynamodbConfigTypeDef = TypedDict(
    "_OptionalClientUpdateDataSourcedynamodbConfigTypeDef",
    {
        "useCallerCredentials": bool,
        "deltaSyncConfig": ClientUpdateDataSourcedynamodbConfigdeltaSyncConfigTypeDef,
        "versioned": bool,
    },
    total=False,
)


class ClientUpdateDataSourcedynamodbConfigTypeDef(
    _RequiredClientUpdateDataSourcedynamodbConfigTypeDef,
    _OptionalClientUpdateDataSourcedynamodbConfigTypeDef,
):
    """
    Type definition for `ClientUpdateDataSource` `dynamodbConfig`

    The new Amazon DynamoDB configuration.

    - **tableName** *(string) --* **[REQUIRED]**

      The table name.

    - **awsRegion** *(string) --* **[REQUIRED]**

      The AWS Region.

    - **useCallerCredentials** *(boolean) --*

      Set to TRUE to use Amazon Cognito credentials with this data source.

    - **deltaSyncConfig** *(dict) --*

      The ``DeltaSyncConfig`` for a versioned datasource.

      - **baseTableTTL** *(integer) --*

        The number of minutes an Item is stored in the datasource.

      - **deltaSyncTableName** *(string) --*

        The Delta Sync table name.

      - **deltaSyncTableTTL** *(integer) --*

        The number of minutes a Delta Sync log entry is stored in the Delta Sync table.

    - **versioned** *(boolean) --*

      Set to TRUE to use Conflict Detection and Resolution with this data source.
    """


_ClientUpdateDataSourceelasticsearchConfigTypeDef = TypedDict(
    "_ClientUpdateDataSourceelasticsearchConfigTypeDef", {"endpoint": str, "awsRegion": str}
)


class ClientUpdateDataSourceelasticsearchConfigTypeDef(
    _ClientUpdateDataSourceelasticsearchConfigTypeDef
):
    """
    Type definition for `ClientUpdateDataSource` `elasticsearchConfig`

    The new Elasticsearch Service configuration.

    - **endpoint** *(string) --* **[REQUIRED]**

      The endpoint.

    - **awsRegion** *(string) --* **[REQUIRED]**

      The AWS Region.
    """


_ClientUpdateDataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef = TypedDict(
    "_ClientUpdateDataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef",
    {"signingRegion": str, "signingServiceName": str},
    total=False,
)


class ClientUpdateDataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef(
    _ClientUpdateDataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef
):
    """
    Type definition for `ClientUpdateDataSourcehttpConfigauthorizationConfig` `awsIamConfig`

    The AWS IAM settings.

    - **signingRegion** *(string) --*

      The signing region for AWS IAM authorization.

    - **signingServiceName** *(string) --*

      The signing service name for AWS IAM authorization.
    """


_RequiredClientUpdateDataSourcehttpConfigauthorizationConfigTypeDef = TypedDict(
    "_RequiredClientUpdateDataSourcehttpConfigauthorizationConfigTypeDef",
    {"authorizationType": str},
)
_OptionalClientUpdateDataSourcehttpConfigauthorizationConfigTypeDef = TypedDict(
    "_OptionalClientUpdateDataSourcehttpConfigauthorizationConfigTypeDef",
    {"awsIamConfig": ClientUpdateDataSourcehttpConfigauthorizationConfigawsIamConfigTypeDef},
    total=False,
)


class ClientUpdateDataSourcehttpConfigauthorizationConfigTypeDef(
    _RequiredClientUpdateDataSourcehttpConfigauthorizationConfigTypeDef,
    _OptionalClientUpdateDataSourcehttpConfigauthorizationConfigTypeDef,
):
    """
    Type definition for `ClientUpdateDataSourcehttpConfig` `authorizationConfig`

    The authorization config in case the HTTP endpoint requires authorization.

    - **authorizationType** *(string) --* **[REQUIRED]**

      The authorization type required by the HTTP endpoint.

      * **AWS_IAM** : The authorization type is Sigv4.

    - **awsIamConfig** *(dict) --*

      The AWS IAM settings.

      - **signingRegion** *(string) --*

        The signing region for AWS IAM authorization.

      - **signingServiceName** *(string) --*

        The signing service name for AWS IAM authorization.
    """


_ClientUpdateDataSourcehttpConfigTypeDef = TypedDict(
    "_ClientUpdateDataSourcehttpConfigTypeDef",
    {
        "endpoint": str,
        "authorizationConfig": ClientUpdateDataSourcehttpConfigauthorizationConfigTypeDef,
    },
    total=False,
)


class ClientUpdateDataSourcehttpConfigTypeDef(_ClientUpdateDataSourcehttpConfigTypeDef):
    """
    Type definition for `ClientUpdateDataSource` `httpConfig`

    The new HTTP endpoint configuration.

    - **endpoint** *(string) --*

      The HTTP URL endpoint. You can either specify the domain name or IP, and port combination, and
      the URL scheme must be HTTP or HTTPS. If the port is not specified, AWS AppSync uses the
      default port 80 for the HTTP endpoint and port 443 for HTTPS endpoints.

    - **authorizationConfig** *(dict) --*

      The authorization config in case the HTTP endpoint requires authorization.

      - **authorizationType** *(string) --* **[REQUIRED]**

        The authorization type required by the HTTP endpoint.

        * **AWS_IAM** : The authorization type is Sigv4.

      - **awsIamConfig** *(dict) --*

        The AWS IAM settings.

        - **signingRegion** *(string) --*

          The signing region for AWS IAM authorization.

        - **signingServiceName** *(string) --*

          The signing service name for AWS IAM authorization.
    """


_ClientUpdateDataSourcelambdaConfigTypeDef = TypedDict(
    "_ClientUpdateDataSourcelambdaConfigTypeDef", {"lambdaFunctionArn": str}
)


class ClientUpdateDataSourcelambdaConfigTypeDef(_ClientUpdateDataSourcelambdaConfigTypeDef):
    """
    Type definition for `ClientUpdateDataSource` `lambdaConfig`

    The new AWS Lambda configuration.

    - **lambdaFunctionArn** *(string) --* **[REQUIRED]**

      The ARN for the Lambda function.
    """


_ClientUpdateDataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef = TypedDict(
    "_ClientUpdateDataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef",
    {
        "awsRegion": str,
        "dbClusterIdentifier": str,
        "databaseName": str,
        "schema": str,
        "awsSecretStoreArn": str,
    },
    total=False,
)


class ClientUpdateDataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef(
    _ClientUpdateDataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef
):
    """
    Type definition for `ClientUpdateDataSourcerelationalDatabaseConfig` `rdsHttpEndpointConfig`

    Amazon RDS HTTP endpoint settings.

    - **awsRegion** *(string) --*

      AWS Region for RDS HTTP endpoint.

    - **dbClusterIdentifier** *(string) --*

      Amazon RDS cluster identifier.

    - **databaseName** *(string) --*

      Logical database name.

    - **schema** *(string) --*

      Logical schema name.

    - **awsSecretStoreArn** *(string) --*

      AWS secret store ARN for database credentials.
    """


_ClientUpdateDataSourcerelationalDatabaseConfigTypeDef = TypedDict(
    "_ClientUpdateDataSourcerelationalDatabaseConfigTypeDef",
    {
        "relationalDatabaseSourceType": str,
        "rdsHttpEndpointConfig": ClientUpdateDataSourcerelationalDatabaseConfigrdsHttpEndpointConfigTypeDef,
    },
    total=False,
)


class ClientUpdateDataSourcerelationalDatabaseConfigTypeDef(
    _ClientUpdateDataSourcerelationalDatabaseConfigTypeDef
):
    """
    Type definition for `ClientUpdateDataSource` `relationalDatabaseConfig`

    The new relational database configuration.

    - **relationalDatabaseSourceType** *(string) --*

      Source type for the relational database.

      * **RDS_HTTP_ENDPOINT** : The relational database source type is an Amazon RDS HTTP endpoint.

    - **rdsHttpEndpointConfig** *(dict) --*

      Amazon RDS HTTP endpoint settings.

      - **awsRegion** *(string) --*

        AWS Region for RDS HTTP endpoint.

      - **dbClusterIdentifier** *(string) --*

        Amazon RDS cluster identifier.

      - **databaseName** *(string) --*

        Logical database name.

      - **schema** *(string) --*

        Logical schema name.

      - **awsSecretStoreArn** *(string) --*

        AWS secret store ARN for database credentials.
    """


_ClientUpdateFunctionResponsefunctionConfigurationTypeDef = TypedDict(
    "_ClientUpdateFunctionResponsefunctionConfigurationTypeDef",
    {
        "functionId": str,
        "functionArn": str,
        "name": str,
        "description": str,
        "dataSourceName": str,
        "requestMappingTemplate": str,
        "responseMappingTemplate": str,
        "functionVersion": str,
    },
    total=False,
)


class ClientUpdateFunctionResponsefunctionConfigurationTypeDef(
    _ClientUpdateFunctionResponsefunctionConfigurationTypeDef
):
    """
    Type definition for `ClientUpdateFunctionResponse` `functionConfiguration`

    The ``Function`` object.

    - **functionId** *(string) --*

      A unique ID representing the ``Function`` object.

    - **functionArn** *(string) --*

      The ARN of the ``Function`` object.

    - **name** *(string) --*

      The name of the ``Function`` object.

    - **description** *(string) --*

      The ``Function`` description.

    - **dataSourceName** *(string) --*

      The name of the ``DataSource`` .

    - **requestMappingTemplate** *(string) --*

      The ``Function`` request mapping template. Functions support only the 2018-05-29 version of
      the request mapping template.

    - **responseMappingTemplate** *(string) --*

      The ``Function`` response mapping template.

    - **functionVersion** *(string) --*

      The version of the request mapping template. Currently only the 2018-05-29 version of the
      template is supported.
    """


_ClientUpdateFunctionResponseTypeDef = TypedDict(
    "_ClientUpdateFunctionResponseTypeDef",
    {"functionConfiguration": ClientUpdateFunctionResponsefunctionConfigurationTypeDef},
    total=False,
)


class ClientUpdateFunctionResponseTypeDef(_ClientUpdateFunctionResponseTypeDef):
    """
    Type definition for `ClientUpdateFunction` `Response`

    - **functionConfiguration** *(dict) --*

      The ``Function`` object.

      - **functionId** *(string) --*

        A unique ID representing the ``Function`` object.

      - **functionArn** *(string) --*

        The ARN of the ``Function`` object.

      - **name** *(string) --*

        The name of the ``Function`` object.

      - **description** *(string) --*

        The ``Function`` description.

      - **dataSourceName** *(string) --*

        The name of the ``DataSource`` .

      - **requestMappingTemplate** *(string) --*

        The ``Function`` request mapping template. Functions support only the 2018-05-29 version of
        the request mapping template.

      - **responseMappingTemplate** *(string) --*

        The ``Function`` response mapping template.

      - **functionVersion** *(string) --*

        The version of the request mapping template. Currently only the 2018-05-29 version of the
        template is supported.
    """


_ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef = TypedDict(
    "_ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef",
    {"issuer": str, "clientId": str, "iatTTL": int, "authTTL": int},
    total=False,
)


class ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef(
    _ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef
):
    """
    Type definition for `ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProviders`
    `openIDConnectConfig`

    The OpenID Connect configuration.

    - **issuer** *(string) --*

      The issuer for the OpenID Connect configuration. The issuer returned by discovery must exactly
      match the value of ``iss`` in the ID token.

    - **clientId** *(string) --*

      The client identifier of the Relying party at the OpenID identity provider. This identifier is
      typically obtained when the Relying party is registered with the OpenID identity provider. You
      can specify a regular expression so the AWS AppSync can validate against multiple client
      identifiers at a time.

    - **iatTTL** *(integer) --*

      The number of milliseconds a token is valid after being issued to a user.

    - **authTTL** *(integer) --*

      The number of milliseconds a token is valid after being authenticated.
    """


_ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef = TypedDict(
    "_ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef",
    {"userPoolId": str, "awsRegion": str, "appIdClientRegex": str},
    total=False,
)


class ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef(
    _ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef
):
    """
    Type definition for `ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProviders`
    `userPoolConfig`

    The Amazon Cognito user pool configuration.

    - **userPoolId** *(string) --*

      The user pool ID.

    - **awsRegion** *(string) --*

      The AWS Region in which the user pool was created.

    - **appIdClientRegex** *(string) --*

      A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersTypeDef = TypedDict(
    "_ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersTypeDef",
    {
        "authenticationType": str,
        "openIDConnectConfig": ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef,
        "userPoolConfig": ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef,
    },
    total=False,
)


class ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersTypeDef(
    _ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersTypeDef
):
    """
    Type definition for `ClientUpdateGraphqlApiResponsegraphqlApi`
    `additionalAuthenticationProviders`

    Describes an additional authentication provider.

    - **authenticationType** *(string) --*

      The authentication type: API key, AWS IAM, OIDC, or Amazon Cognito user pools.

    - **openIDConnectConfig** *(dict) --*

      The OpenID Connect configuration.

      - **issuer** *(string) --*

        The issuer for the OpenID Connect configuration. The issuer returned by discovery must
        exactly match the value of ``iss`` in the ID token.

      - **clientId** *(string) --*

        The client identifier of the Relying party at the OpenID identity provider. This identifier
        is typically obtained when the Relying party is registered with the OpenID identity
        provider. You can specify a regular expression so the AWS AppSync can validate against
        multiple client identifiers at a time.

      - **iatTTL** *(integer) --*

        The number of milliseconds a token is valid after being issued to a user.

      - **authTTL** *(integer) --*

        The number of milliseconds a token is valid after being authenticated.

    - **userPoolConfig** *(dict) --*

      The Amazon Cognito user pool configuration.

      - **userPoolId** *(string) --*

        The user pool ID.

      - **awsRegion** *(string) --*

        The AWS Region in which the user pool was created.

      - **appIdClientRegex** *(string) --*

        A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientUpdateGraphqlApiResponsegraphqlApilogConfigTypeDef = TypedDict(
    "_ClientUpdateGraphqlApiResponsegraphqlApilogConfigTypeDef",
    {"fieldLogLevel": str, "cloudWatchLogsRoleArn": str, "excludeVerboseContent": bool},
    total=False,
)


class ClientUpdateGraphqlApiResponsegraphqlApilogConfigTypeDef(
    _ClientUpdateGraphqlApiResponsegraphqlApilogConfigTypeDef
):
    """
    Type definition for `ClientUpdateGraphqlApiResponsegraphqlApi` `logConfig`

    The Amazon CloudWatch Logs configuration.

    - **fieldLogLevel** *(string) --*

      The field logging level. Values can be NONE, ERROR, or ALL.

      * **NONE** : No field-level logs are captured.

      * **ERROR** : Logs the following information only for the fields that are in error:

        * The error section in the server response.

        * Field-level errors.

        * The generated request/response functions that got resolved for error fields.

      * **ALL** : The following information is logged for all fields in the query:

        * Field-level tracing information.

        * The generated request/response functions that got resolved for each field.

    - **cloudWatchLogsRoleArn** *(string) --*

      The service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in your
      account.

    - **excludeVerboseContent** *(boolean) --*

      Set to TRUE to exclude sections that contain information such as headers, context, and
      evaluated mapping templates, regardless of logging level.
    """


_ClientUpdateGraphqlApiResponsegraphqlApiopenIDConnectConfigTypeDef = TypedDict(
    "_ClientUpdateGraphqlApiResponsegraphqlApiopenIDConnectConfigTypeDef",
    {"issuer": str, "clientId": str, "iatTTL": int, "authTTL": int},
    total=False,
)


class ClientUpdateGraphqlApiResponsegraphqlApiopenIDConnectConfigTypeDef(
    _ClientUpdateGraphqlApiResponsegraphqlApiopenIDConnectConfigTypeDef
):
    """
    Type definition for `ClientUpdateGraphqlApiResponsegraphqlApi` `openIDConnectConfig`

    The OpenID Connect configuration.

    - **issuer** *(string) --*

      The issuer for the OpenID Connect configuration. The issuer returned by discovery must exactly
      match the value of ``iss`` in the ID token.

    - **clientId** *(string) --*

      The client identifier of the Relying party at the OpenID identity provider. This identifier is
      typically obtained when the Relying party is registered with the OpenID identity provider. You
      can specify a regular expression so the AWS AppSync can validate against multiple client
      identifiers at a time.

    - **iatTTL** *(integer) --*

      The number of milliseconds a token is valid after being issued to a user.

    - **authTTL** *(integer) --*

      The number of milliseconds a token is valid after being authenticated.
    """


_ClientUpdateGraphqlApiResponsegraphqlApiuserPoolConfigTypeDef = TypedDict(
    "_ClientUpdateGraphqlApiResponsegraphqlApiuserPoolConfigTypeDef",
    {"userPoolId": str, "awsRegion": str, "defaultAction": str, "appIdClientRegex": str},
    total=False,
)


class ClientUpdateGraphqlApiResponsegraphqlApiuserPoolConfigTypeDef(
    _ClientUpdateGraphqlApiResponsegraphqlApiuserPoolConfigTypeDef
):
    """
    Type definition for `ClientUpdateGraphqlApiResponsegraphqlApi` `userPoolConfig`

    The Amazon Cognito user pool configuration.

    - **userPoolId** *(string) --*

      The user pool ID.

    - **awsRegion** *(string) --*

      The AWS Region in which the user pool was created.

    - **defaultAction** *(string) --*

      The action that you want your GraphQL API to take when a request that uses Amazon Cognito user
      pool authentication doesn't match the Amazon Cognito user pool configuration.

    - **appIdClientRegex** *(string) --*

      A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientUpdateGraphqlApiResponsegraphqlApiTypeDef = TypedDict(
    "_ClientUpdateGraphqlApiResponsegraphqlApiTypeDef",
    {
        "name": str,
        "apiId": str,
        "authenticationType": str,
        "logConfig": ClientUpdateGraphqlApiResponsegraphqlApilogConfigTypeDef,
        "userPoolConfig": ClientUpdateGraphqlApiResponsegraphqlApiuserPoolConfigTypeDef,
        "openIDConnectConfig": ClientUpdateGraphqlApiResponsegraphqlApiopenIDConnectConfigTypeDef,
        "arn": str,
        "uris": Dict[str, str],
        "tags": Dict[str, str],
        "additionalAuthenticationProviders": List[
            ClientUpdateGraphqlApiResponsegraphqlApiadditionalAuthenticationProvidersTypeDef
        ],
    },
    total=False,
)


class ClientUpdateGraphqlApiResponsegraphqlApiTypeDef(
    _ClientUpdateGraphqlApiResponsegraphqlApiTypeDef
):
    """
    Type definition for `ClientUpdateGraphqlApiResponse` `graphqlApi`

    The updated ``GraphqlApi`` object.

    - **name** *(string) --*

      The API name.

    - **apiId** *(string) --*

      The API ID.

    - **authenticationType** *(string) --*

      The authentication type.

    - **logConfig** *(dict) --*

      The Amazon CloudWatch Logs configuration.

      - **fieldLogLevel** *(string) --*

        The field logging level. Values can be NONE, ERROR, or ALL.

        * **NONE** : No field-level logs are captured.

        * **ERROR** : Logs the following information only for the fields that are in error:

          * The error section in the server response.

          * Field-level errors.

          * The generated request/response functions that got resolved for error fields.

        * **ALL** : The following information is logged for all fields in the query:

          * Field-level tracing information.

          * The generated request/response functions that got resolved for each field.

      - **cloudWatchLogsRoleArn** *(string) --*

        The service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in your
        account.

      - **excludeVerboseContent** *(boolean) --*

        Set to TRUE to exclude sections that contain information such as headers, context, and
        evaluated mapping templates, regardless of logging level.

    - **userPoolConfig** *(dict) --*

      The Amazon Cognito user pool configuration.

      - **userPoolId** *(string) --*

        The user pool ID.

      - **awsRegion** *(string) --*

        The AWS Region in which the user pool was created.

      - **defaultAction** *(string) --*

        The action that you want your GraphQL API to take when a request that uses Amazon Cognito
        user pool authentication doesn't match the Amazon Cognito user pool configuration.

      - **appIdClientRegex** *(string) --*

        A regular expression for validating the incoming Amazon Cognito user pool app client ID.

    - **openIDConnectConfig** *(dict) --*

      The OpenID Connect configuration.

      - **issuer** *(string) --*

        The issuer for the OpenID Connect configuration. The issuer returned by discovery must
        exactly match the value of ``iss`` in the ID token.

      - **clientId** *(string) --*

        The client identifier of the Relying party at the OpenID identity provider. This identifier
        is typically obtained when the Relying party is registered with the OpenID identity
        provider. You can specify a regular expression so the AWS AppSync can validate against
        multiple client identifiers at a time.

      - **iatTTL** *(integer) --*

        The number of milliseconds a token is valid after being issued to a user.

      - **authTTL** *(integer) --*

        The number of milliseconds a token is valid after being authenticated.

    - **arn** *(string) --*

      The ARN.

    - **uris** *(dict) --*

      The URIs.

      - *(string) --*

        - *(string) --*

    - **tags** *(dict) --*

      The tags.

      - *(string) --*

        The key for the tag.

        - *(string) --*

          The value for the tag.

    - **additionalAuthenticationProviders** *(list) --*

      A list of additional authentication providers for the ``GraphqlApi`` API.

      - *(dict) --*

        Describes an additional authentication provider.

        - **authenticationType** *(string) --*

          The authentication type: API key, AWS IAM, OIDC, or Amazon Cognito user pools.

        - **openIDConnectConfig** *(dict) --*

          The OpenID Connect configuration.

          - **issuer** *(string) --*

            The issuer for the OpenID Connect configuration. The issuer returned by discovery must
            exactly match the value of ``iss`` in the ID token.

          - **clientId** *(string) --*

            The client identifier of the Relying party at the OpenID identity provider. This
            identifier is typically obtained when the Relying party is registered with the OpenID
            identity provider. You can specify a regular expression so the AWS AppSync can validate
            against multiple client identifiers at a time.

          - **iatTTL** *(integer) --*

            The number of milliseconds a token is valid after being issued to a user.

          - **authTTL** *(integer) --*

            The number of milliseconds a token is valid after being authenticated.

        - **userPoolConfig** *(dict) --*

          The Amazon Cognito user pool configuration.

          - **userPoolId** *(string) --*

            The user pool ID.

          - **awsRegion** *(string) --*

            The AWS Region in which the user pool was created.

          - **appIdClientRegex** *(string) --*

            A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientUpdateGraphqlApiResponseTypeDef = TypedDict(
    "_ClientUpdateGraphqlApiResponseTypeDef",
    {"graphqlApi": ClientUpdateGraphqlApiResponsegraphqlApiTypeDef},
    total=False,
)


class ClientUpdateGraphqlApiResponseTypeDef(_ClientUpdateGraphqlApiResponseTypeDef):
    """
    Type definition for `ClientUpdateGraphqlApi` `Response`

    - **graphqlApi** *(dict) --*

      The updated ``GraphqlApi`` object.

      - **name** *(string) --*

        The API name.

      - **apiId** *(string) --*

        The API ID.

      - **authenticationType** *(string) --*

        The authentication type.

      - **logConfig** *(dict) --*

        The Amazon CloudWatch Logs configuration.

        - **fieldLogLevel** *(string) --*

          The field logging level. Values can be NONE, ERROR, or ALL.

          * **NONE** : No field-level logs are captured.

          * **ERROR** : Logs the following information only for the fields that are in error:

            * The error section in the server response.

            * Field-level errors.

            * The generated request/response functions that got resolved for error fields.

          * **ALL** : The following information is logged for all fields in the query:

            * Field-level tracing information.

            * The generated request/response functions that got resolved for each field.

        - **cloudWatchLogsRoleArn** *(string) --*

          The service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in your
          account.

        - **excludeVerboseContent** *(boolean) --*

          Set to TRUE to exclude sections that contain information such as headers, context, and
          evaluated mapping templates, regardless of logging level.

      - **userPoolConfig** *(dict) --*

        The Amazon Cognito user pool configuration.

        - **userPoolId** *(string) --*

          The user pool ID.

        - **awsRegion** *(string) --*

          The AWS Region in which the user pool was created.

        - **defaultAction** *(string) --*

          The action that you want your GraphQL API to take when a request that uses Amazon Cognito
          user pool authentication doesn't match the Amazon Cognito user pool configuration.

        - **appIdClientRegex** *(string) --*

          A regular expression for validating the incoming Amazon Cognito user pool app client ID.

      - **openIDConnectConfig** *(dict) --*

        The OpenID Connect configuration.

        - **issuer** *(string) --*

          The issuer for the OpenID Connect configuration. The issuer returned by discovery must
          exactly match the value of ``iss`` in the ID token.

        - **clientId** *(string) --*

          The client identifier of the Relying party at the OpenID identity provider. This
          identifier is typically obtained when the Relying party is registered with the OpenID
          identity provider. You can specify a regular expression so the AWS AppSync can validate
          against multiple client identifiers at a time.

        - **iatTTL** *(integer) --*

          The number of milliseconds a token is valid after being issued to a user.

        - **authTTL** *(integer) --*

          The number of milliseconds a token is valid after being authenticated.

      - **arn** *(string) --*

        The ARN.

      - **uris** *(dict) --*

        The URIs.

        - *(string) --*

          - *(string) --*

      - **tags** *(dict) --*

        The tags.

        - *(string) --*

          The key for the tag.

          - *(string) --*

            The value for the tag.

      - **additionalAuthenticationProviders** *(list) --*

        A list of additional authentication providers for the ``GraphqlApi`` API.

        - *(dict) --*

          Describes an additional authentication provider.

          - **authenticationType** *(string) --*

            The authentication type: API key, AWS IAM, OIDC, or Amazon Cognito user pools.

          - **openIDConnectConfig** *(dict) --*

            The OpenID Connect configuration.

            - **issuer** *(string) --*

              The issuer for the OpenID Connect configuration. The issuer returned by discovery must
              exactly match the value of ``iss`` in the ID token.

            - **clientId** *(string) --*

              The client identifier of the Relying party at the OpenID identity provider. This
              identifier is typically obtained when the Relying party is registered with the OpenID
              identity provider. You can specify a regular expression so the AWS AppSync can
              validate against multiple client identifiers at a time.

            - **iatTTL** *(integer) --*

              The number of milliseconds a token is valid after being issued to a user.

            - **authTTL** *(integer) --*

              The number of milliseconds a token is valid after being authenticated.

          - **userPoolConfig** *(dict) --*

            The Amazon Cognito user pool configuration.

            - **userPoolId** *(string) --*

              The user pool ID.

            - **awsRegion** *(string) --*

              The AWS Region in which the user pool was created.

            - **appIdClientRegex** *(string) --*

              A regular expression for validating the incoming Amazon Cognito user pool app client
              ID.
    """


_RequiredClientUpdateGraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef = TypedDict(
    "_RequiredClientUpdateGraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef",
    {"issuer": str},
)
_OptionalClientUpdateGraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef = TypedDict(
    "_OptionalClientUpdateGraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef",
    {"clientId": str, "iatTTL": int, "authTTL": int},
    total=False,
)


class ClientUpdateGraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef(
    _RequiredClientUpdateGraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef,
    _OptionalClientUpdateGraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef,
):
    """
    Type definition for `ClientUpdateGraphqlApiadditionalAuthenticationProviders`
    `openIDConnectConfig`

    The OpenID Connect configuration.

    - **issuer** *(string) --* **[REQUIRED]**

      The issuer for the OpenID Connect configuration. The issuer returned by discovery must exactly
      match the value of ``iss`` in the ID token.

    - **clientId** *(string) --*

      The client identifier of the Relying party at the OpenID identity provider. This identifier is
      typically obtained when the Relying party is registered with the OpenID identity provider. You
      can specify a regular expression so the AWS AppSync can validate against multiple client
      identifiers at a time.

    - **iatTTL** *(integer) --*

      The number of milliseconds a token is valid after being issued to a user.

    - **authTTL** *(integer) --*

      The number of milliseconds a token is valid after being authenticated.
    """


_RequiredClientUpdateGraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef = TypedDict(
    "_RequiredClientUpdateGraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef",
    {"userPoolId": str, "awsRegion": str},
)
_OptionalClientUpdateGraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef = TypedDict(
    "_OptionalClientUpdateGraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef",
    {"appIdClientRegex": str},
    total=False,
)


class ClientUpdateGraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef(
    _RequiredClientUpdateGraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef,
    _OptionalClientUpdateGraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef,
):
    """
    Type definition for `ClientUpdateGraphqlApiadditionalAuthenticationProviders` `userPoolConfig`

    The Amazon Cognito user pool configuration.

    - **userPoolId** *(string) --* **[REQUIRED]**

      The user pool ID.

    - **awsRegion** *(string) --* **[REQUIRED]**

      The AWS Region in which the user pool was created.

    - **appIdClientRegex** *(string) --*

      A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientUpdateGraphqlApiadditionalAuthenticationProvidersTypeDef = TypedDict(
    "_ClientUpdateGraphqlApiadditionalAuthenticationProvidersTypeDef",
    {
        "authenticationType": str,
        "openIDConnectConfig": ClientUpdateGraphqlApiadditionalAuthenticationProvidersopenIDConnectConfigTypeDef,
        "userPoolConfig": ClientUpdateGraphqlApiadditionalAuthenticationProvidersuserPoolConfigTypeDef,
    },
    total=False,
)


class ClientUpdateGraphqlApiadditionalAuthenticationProvidersTypeDef(
    _ClientUpdateGraphqlApiadditionalAuthenticationProvidersTypeDef
):
    """
    Type definition for `ClientUpdateGraphqlApi` `additionalAuthenticationProviders`

    Describes an additional authentication provider.

    - **authenticationType** *(string) --*

      The authentication type: API key, AWS IAM, OIDC, or Amazon Cognito user pools.

    - **openIDConnectConfig** *(dict) --*

      The OpenID Connect configuration.

      - **issuer** *(string) --* **[REQUIRED]**

        The issuer for the OpenID Connect configuration. The issuer returned by discovery must
        exactly match the value of ``iss`` in the ID token.

      - **clientId** *(string) --*

        The client identifier of the Relying party at the OpenID identity provider. This identifier
        is typically obtained when the Relying party is registered with the OpenID identity
        provider. You can specify a regular expression so the AWS AppSync can validate against
        multiple client identifiers at a time.

      - **iatTTL** *(integer) --*

        The number of milliseconds a token is valid after being issued to a user.

      - **authTTL** *(integer) --*

        The number of milliseconds a token is valid after being authenticated.

    - **userPoolConfig** *(dict) --*

      The Amazon Cognito user pool configuration.

      - **userPoolId** *(string) --* **[REQUIRED]**

        The user pool ID.

      - **awsRegion** *(string) --* **[REQUIRED]**

        The AWS Region in which the user pool was created.

      - **appIdClientRegex** *(string) --*

        A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_RequiredClientUpdateGraphqlApilogConfigTypeDef = TypedDict(
    "_RequiredClientUpdateGraphqlApilogConfigTypeDef",
    {"fieldLogLevel": str, "cloudWatchLogsRoleArn": str},
)
_OptionalClientUpdateGraphqlApilogConfigTypeDef = TypedDict(
    "_OptionalClientUpdateGraphqlApilogConfigTypeDef", {"excludeVerboseContent": bool}, total=False
)


class ClientUpdateGraphqlApilogConfigTypeDef(
    _RequiredClientUpdateGraphqlApilogConfigTypeDef, _OptionalClientUpdateGraphqlApilogConfigTypeDef
):
    """
    Type definition for `ClientUpdateGraphqlApi` `logConfig`

    The Amazon CloudWatch Logs configuration for the ``GraphqlApi`` object.

    - **fieldLogLevel** *(string) --* **[REQUIRED]**

      The field logging level. Values can be NONE, ERROR, or ALL.

      * **NONE** : No field-level logs are captured.

      * **ERROR** : Logs the following information only for the fields that are in error:

        * The error section in the server response.

        * Field-level errors.

        * The generated request/response functions that got resolved for error fields.

      * **ALL** : The following information is logged for all fields in the query:

        * Field-level tracing information.

        * The generated request/response functions that got resolved for each field.

    - **cloudWatchLogsRoleArn** *(string) --* **[REQUIRED]**

      The service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in your
      account.

    - **excludeVerboseContent** *(boolean) --*

      Set to TRUE to exclude sections that contain information such as headers, context, and
      evaluated mapping templates, regardless of logging level.
    """


_RequiredClientUpdateGraphqlApiopenIDConnectConfigTypeDef = TypedDict(
    "_RequiredClientUpdateGraphqlApiopenIDConnectConfigTypeDef", {"issuer": str}
)
_OptionalClientUpdateGraphqlApiopenIDConnectConfigTypeDef = TypedDict(
    "_OptionalClientUpdateGraphqlApiopenIDConnectConfigTypeDef",
    {"clientId": str, "iatTTL": int, "authTTL": int},
    total=False,
)


class ClientUpdateGraphqlApiopenIDConnectConfigTypeDef(
    _RequiredClientUpdateGraphqlApiopenIDConnectConfigTypeDef,
    _OptionalClientUpdateGraphqlApiopenIDConnectConfigTypeDef,
):
    """
    Type definition for `ClientUpdateGraphqlApi` `openIDConnectConfig`

    The OpenID Connect configuration for the ``GraphqlApi`` object.

    - **issuer** *(string) --* **[REQUIRED]**

      The issuer for the OpenID Connect configuration. The issuer returned by discovery must exactly
      match the value of ``iss`` in the ID token.

    - **clientId** *(string) --*

      The client identifier of the Relying party at the OpenID identity provider. This identifier is
      typically obtained when the Relying party is registered with the OpenID identity provider. You
      can specify a regular expression so the AWS AppSync can validate against multiple client
      identifiers at a time.

    - **iatTTL** *(integer) --*

      The number of milliseconds a token is valid after being issued to a user.

    - **authTTL** *(integer) --*

      The number of milliseconds a token is valid after being authenticated.
    """


_RequiredClientUpdateGraphqlApiuserPoolConfigTypeDef = TypedDict(
    "_RequiredClientUpdateGraphqlApiuserPoolConfigTypeDef",
    {"userPoolId": str, "awsRegion": str, "defaultAction": str},
)
_OptionalClientUpdateGraphqlApiuserPoolConfigTypeDef = TypedDict(
    "_OptionalClientUpdateGraphqlApiuserPoolConfigTypeDef", {"appIdClientRegex": str}, total=False
)


class ClientUpdateGraphqlApiuserPoolConfigTypeDef(
    _RequiredClientUpdateGraphqlApiuserPoolConfigTypeDef,
    _OptionalClientUpdateGraphqlApiuserPoolConfigTypeDef,
):
    """
    Type definition for `ClientUpdateGraphqlApi` `userPoolConfig`

    The new Amazon Cognito user pool configuration for the ``GraphqlApi`` object.

    - **userPoolId** *(string) --* **[REQUIRED]**

      The user pool ID.

    - **awsRegion** *(string) --* **[REQUIRED]**

      The AWS Region in which the user pool was created.

    - **defaultAction** *(string) --* **[REQUIRED]**

      The action that you want your GraphQL API to take when a request that uses Amazon Cognito user
      pool authentication doesn't match the Amazon Cognito user pool configuration.

    - **appIdClientRegex** *(string) --*

      A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ClientUpdateResolverResponseresolvercachingConfigTypeDef = TypedDict(
    "_ClientUpdateResolverResponseresolvercachingConfigTypeDef",
    {"ttl": int, "cachingKeys": List[str]},
    total=False,
)


class ClientUpdateResolverResponseresolvercachingConfigTypeDef(
    _ClientUpdateResolverResponseresolvercachingConfigTypeDef
):
    """
    Type definition for `ClientUpdateResolverResponseresolver` `cachingConfig`

    The caching configuration for the resolver.

    - **ttl** *(integer) --*

      The TTL in seconds for a resolver that has caching enabled.

      Valid values are between 1 and 3600 seconds.

    - **cachingKeys** *(list) --*

      The caching keys for a resolver that has caching enabled.

      Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

      - *(string) --*
    """


_ClientUpdateResolverResponseresolverpipelineConfigTypeDef = TypedDict(
    "_ClientUpdateResolverResponseresolverpipelineConfigTypeDef",
    {"functions": List[str]},
    total=False,
)


class ClientUpdateResolverResponseresolverpipelineConfigTypeDef(
    _ClientUpdateResolverResponseresolverpipelineConfigTypeDef
):
    """
    Type definition for `ClientUpdateResolverResponseresolver` `pipelineConfig`

    The ``PipelineConfig`` .

    - **functions** *(list) --*

      A list of ``Function`` objects.

      - *(string) --*
    """


_ClientUpdateResolverResponseresolversyncConfiglambdaConflictHandlerConfigTypeDef = TypedDict(
    "_ClientUpdateResolverResponseresolversyncConfiglambdaConflictHandlerConfigTypeDef",
    {"lambdaConflictHandlerArn": str},
    total=False,
)


class ClientUpdateResolverResponseresolversyncConfiglambdaConflictHandlerConfigTypeDef(
    _ClientUpdateResolverResponseresolversyncConfiglambdaConflictHandlerConfigTypeDef
):
    """
    Type definition for `ClientUpdateResolverResponseresolversyncConfig`
    `lambdaConflictHandlerConfig`

    The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

    - **lambdaConflictHandlerArn** *(string) --*

      The Arn for the Lambda function to use as the Conflict Handler.
    """


_ClientUpdateResolverResponseresolversyncConfigTypeDef = TypedDict(
    "_ClientUpdateResolverResponseresolversyncConfigTypeDef",
    {
        "conflictHandler": str,
        "conflictDetection": str,
        "lambdaConflictHandlerConfig": ClientUpdateResolverResponseresolversyncConfiglambdaConflictHandlerConfigTypeDef,
    },
    total=False,
)


class ClientUpdateResolverResponseresolversyncConfigTypeDef(
    _ClientUpdateResolverResponseresolversyncConfigTypeDef
):
    """
    Type definition for `ClientUpdateResolverResponseresolver` `syncConfig`

    The ``SyncConfig`` for a resolver attached to a versioned datasource.

    - **conflictHandler** *(string) --*

      The Conflict Resolution strategy to perform in the event of a conflict.

      * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do not
      match the latest version at the server.

      * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

      * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
      LambdaConflictHandlerConfig.

    - **conflictDetection** *(string) --*

      The Conflict Detection strategy to use.

      * **VERSION** : Detect conflicts based on object versions for this resolver.

      * **NONE** : Do not detect conflicts when executing this resolver.

    - **lambdaConflictHandlerConfig** *(dict) --*

      The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

      - **lambdaConflictHandlerArn** *(string) --*

        The Arn for the Lambda function to use as the Conflict Handler.
    """


_ClientUpdateResolverResponseresolverTypeDef = TypedDict(
    "_ClientUpdateResolverResponseresolverTypeDef",
    {
        "typeName": str,
        "fieldName": str,
        "dataSourceName": str,
        "resolverArn": str,
        "requestMappingTemplate": str,
        "responseMappingTemplate": str,
        "kind": str,
        "pipelineConfig": ClientUpdateResolverResponseresolverpipelineConfigTypeDef,
        "syncConfig": ClientUpdateResolverResponseresolversyncConfigTypeDef,
        "cachingConfig": ClientUpdateResolverResponseresolvercachingConfigTypeDef,
    },
    total=False,
)


class ClientUpdateResolverResponseresolverTypeDef(_ClientUpdateResolverResponseresolverTypeDef):
    """
    Type definition for `ClientUpdateResolverResponse` `resolver`

    The updated ``Resolver`` object.

    - **typeName** *(string) --*

      The resolver type name.

    - **fieldName** *(string) --*

      The resolver field name.

    - **dataSourceName** *(string) --*

      The resolver data source name.

    - **resolverArn** *(string) --*

      The resolver ARN.

    - **requestMappingTemplate** *(string) --*

      The request mapping template.

    - **responseMappingTemplate** *(string) --*

      The response mapping template.

    - **kind** *(string) --*

      The resolver type.

      * **UNIT** : A UNIT resolver type. A UNIT resolver is the default resolver type. A UNIT
      resolver enables you to execute a GraphQL query against a single data source.

      * **PIPELINE** : A PIPELINE resolver type. A PIPELINE resolver enables you to execute a series
      of ``Function`` in a serial manner. You can use a pipeline resolver to execute a GraphQL query
      against multiple data sources.

    - **pipelineConfig** *(dict) --*

      The ``PipelineConfig`` .

      - **functions** *(list) --*

        A list of ``Function`` objects.

        - *(string) --*

    - **syncConfig** *(dict) --*

      The ``SyncConfig`` for a resolver attached to a versioned datasource.

      - **conflictHandler** *(string) --*

        The Conflict Resolution strategy to perform in the event of a conflict.

        * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do not
        match the latest version at the server.

        * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

        * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
        LambdaConflictHandlerConfig.

      - **conflictDetection** *(string) --*

        The Conflict Detection strategy to use.

        * **VERSION** : Detect conflicts based on object versions for this resolver.

        * **NONE** : Do not detect conflicts when executing this resolver.

      - **lambdaConflictHandlerConfig** *(dict) --*

        The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

        - **lambdaConflictHandlerArn** *(string) --*

          The Arn for the Lambda function to use as the Conflict Handler.

    - **cachingConfig** *(dict) --*

      The caching configuration for the resolver.

      - **ttl** *(integer) --*

        The TTL in seconds for a resolver that has caching enabled.

        Valid values are between 1 and 3600 seconds.

      - **cachingKeys** *(list) --*

        The caching keys for a resolver that has caching enabled.

        Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

        - *(string) --*
    """


_ClientUpdateResolverResponseTypeDef = TypedDict(
    "_ClientUpdateResolverResponseTypeDef",
    {"resolver": ClientUpdateResolverResponseresolverTypeDef},
    total=False,
)


class ClientUpdateResolverResponseTypeDef(_ClientUpdateResolverResponseTypeDef):
    """
    Type definition for `ClientUpdateResolver` `Response`

    - **resolver** *(dict) --*

      The updated ``Resolver`` object.

      - **typeName** *(string) --*

        The resolver type name.

      - **fieldName** *(string) --*

        The resolver field name.

      - **dataSourceName** *(string) --*

        The resolver data source name.

      - **resolverArn** *(string) --*

        The resolver ARN.

      - **requestMappingTemplate** *(string) --*

        The request mapping template.

      - **responseMappingTemplate** *(string) --*

        The response mapping template.

      - **kind** *(string) --*

        The resolver type.

        * **UNIT** : A UNIT resolver type. A UNIT resolver is the default resolver type. A UNIT
        resolver enables you to execute a GraphQL query against a single data source.

        * **PIPELINE** : A PIPELINE resolver type. A PIPELINE resolver enables you to execute a
        series of ``Function`` in a serial manner. You can use a pipeline resolver to execute a
        GraphQL query against multiple data sources.

      - **pipelineConfig** *(dict) --*

        The ``PipelineConfig`` .

        - **functions** *(list) --*

          A list of ``Function`` objects.

          - *(string) --*

      - **syncConfig** *(dict) --*

        The ``SyncConfig`` for a resolver attached to a versioned datasource.

        - **conflictHandler** *(string) --*

          The Conflict Resolution strategy to perform in the event of a conflict.

          * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do
          not match the latest version at the server.

          * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

          * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
          LambdaConflictHandlerConfig.

        - **conflictDetection** *(string) --*

          The Conflict Detection strategy to use.

          * **VERSION** : Detect conflicts based on object versions for this resolver.

          * **NONE** : Do not detect conflicts when executing this resolver.

        - **lambdaConflictHandlerConfig** *(dict) --*

          The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

          - **lambdaConflictHandlerArn** *(string) --*

            The Arn for the Lambda function to use as the Conflict Handler.

      - **cachingConfig** *(dict) --*

        The caching configuration for the resolver.

        - **ttl** *(integer) --*

          The TTL in seconds for a resolver that has caching enabled.

          Valid values are between 1 and 3600 seconds.

        - **cachingKeys** *(list) --*

          The caching keys for a resolver that has caching enabled.

          Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

          - *(string) --*
    """


_ClientUpdateResolvercachingConfigTypeDef = TypedDict(
    "_ClientUpdateResolvercachingConfigTypeDef", {"ttl": int, "cachingKeys": List[str]}, total=False
)


class ClientUpdateResolvercachingConfigTypeDef(_ClientUpdateResolvercachingConfigTypeDef):
    """
    Type definition for `ClientUpdateResolver` `cachingConfig`

    The caching configuration for the resolver.

    - **ttl** *(integer) --*

      The TTL in seconds for a resolver that has caching enabled.

      Valid values are between 1 and 3600 seconds.

    - **cachingKeys** *(list) --*

      The caching keys for a resolver that has caching enabled.

      Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

      - *(string) --*
    """


_ClientUpdateResolverpipelineConfigTypeDef = TypedDict(
    "_ClientUpdateResolverpipelineConfigTypeDef", {"functions": List[str]}, total=False
)


class ClientUpdateResolverpipelineConfigTypeDef(_ClientUpdateResolverpipelineConfigTypeDef):
    """
    Type definition for `ClientUpdateResolver` `pipelineConfig`

    The ``PipelineConfig`` .

    - **functions** *(list) --*

      A list of ``Function`` objects.

      - *(string) --*
    """


_ClientUpdateResolversyncConfiglambdaConflictHandlerConfigTypeDef = TypedDict(
    "_ClientUpdateResolversyncConfiglambdaConflictHandlerConfigTypeDef",
    {"lambdaConflictHandlerArn": str},
    total=False,
)


class ClientUpdateResolversyncConfiglambdaConflictHandlerConfigTypeDef(
    _ClientUpdateResolversyncConfiglambdaConflictHandlerConfigTypeDef
):
    """
    Type definition for `ClientUpdateResolversyncConfig` `lambdaConflictHandlerConfig`

    The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

    - **lambdaConflictHandlerArn** *(string) --*

      The Arn for the Lambda function to use as the Conflict Handler.
    """


_ClientUpdateResolversyncConfigTypeDef = TypedDict(
    "_ClientUpdateResolversyncConfigTypeDef",
    {
        "conflictHandler": str,
        "conflictDetection": str,
        "lambdaConflictHandlerConfig": ClientUpdateResolversyncConfiglambdaConflictHandlerConfigTypeDef,
    },
    total=False,
)


class ClientUpdateResolversyncConfigTypeDef(_ClientUpdateResolversyncConfigTypeDef):
    """
    Type definition for `ClientUpdateResolver` `syncConfig`

    The ``SyncConfig`` for a resolver attached to a versioned datasource.

    - **conflictHandler** *(string) --*

      The Conflict Resolution strategy to perform in the event of a conflict.

      * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do not
      match the latest version at the server.

      * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

      * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
      LambdaConflictHandlerConfig.

    - **conflictDetection** *(string) --*

      The Conflict Detection strategy to use.

      * **VERSION** : Detect conflicts based on object versions for this resolver.

      * **NONE** : Do not detect conflicts when executing this resolver.

    - **lambdaConflictHandlerConfig** *(dict) --*

      The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

      - **lambdaConflictHandlerArn** *(string) --*

        The Arn for the Lambda function to use as the Conflict Handler.
    """


_ClientUpdateTypeResponsetypeTypeDef = TypedDict(
    "_ClientUpdateTypeResponsetypeTypeDef",
    {"name": str, "description": str, "arn": str, "definition": str, "format": str},
    total=False,
)


class ClientUpdateTypeResponsetypeTypeDef(_ClientUpdateTypeResponsetypeTypeDef):
    """
    Type definition for `ClientUpdateTypeResponse` `type`

    The updated ``Type`` object.

    - **name** *(string) --*

      The type name.

    - **description** *(string) --*

      The type description.

    - **arn** *(string) --*

      The type ARN.

    - **definition** *(string) --*

      The type definition.

    - **format** *(string) --*

      The type format: SDL or JSON.
    """


_ClientUpdateTypeResponseTypeDef = TypedDict(
    "_ClientUpdateTypeResponseTypeDef", {"type": ClientUpdateTypeResponsetypeTypeDef}, total=False
)


class ClientUpdateTypeResponseTypeDef(_ClientUpdateTypeResponseTypeDef):
    """
    Type definition for `ClientUpdateType` `Response`

    - **type** *(dict) --*

      The updated ``Type`` object.

      - **name** *(string) --*

        The type name.

      - **description** *(string) --*

        The type description.

      - **arn** *(string) --*

        The type ARN.

      - **definition** *(string) --*

        The type definition.

      - **format** *(string) --*

        The type format: SDL or JSON.
    """


_ListApiKeysPaginatePaginationConfigTypeDef = TypedDict(
    "_ListApiKeysPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class ListApiKeysPaginatePaginationConfigTypeDef(_ListApiKeysPaginatePaginationConfigTypeDef):
    """
    Type definition for `ListApiKeysPaginate` `PaginationConfig`

    A dictionary that provides parameters to control pagination.

    - **MaxItems** *(integer) --*

      The total number of items to return. If the total number of items available is more than the
      value specified in max-items then a ``NextToken`` will be provided in the output that you can
      use to resume pagination.

    - **PageSize** *(integer) --*

      The size of each page.

    - **StartingToken** *(string) --*

      A token to specify where to start paginating. This is the ``NextToken`` from a previous
      response.
    """


_ListApiKeysPaginateResponseapiKeysTypeDef = TypedDict(
    "_ListApiKeysPaginateResponseapiKeysTypeDef",
    {"id": str, "description": str, "expires": int},
    total=False,
)


class ListApiKeysPaginateResponseapiKeysTypeDef(_ListApiKeysPaginateResponseapiKeysTypeDef):
    """
    Type definition for `ListApiKeysPaginateResponse` `apiKeys`

    Describes an API key.

    Customers invoke AWS AppSync GraphQL API operations with API keys as an identity mechanism.
    There are two key versions:

     **da1** : This version was introduced at launch in November 2017. These keys always expire
     after 7 days. Key expiration is managed by Amazon DynamoDB TTL. The keys ceased to be valid
     after February 21, 2018 and should not be used after that date.

    * ``ListApiKeys`` returns the expiration time in milliseconds.

    * ``CreateApiKey`` returns the expiration time in milliseconds.

    * ``UpdateApiKey`` is not available for this key version.

    * ``DeleteApiKey`` deletes the item from the table.

    * Expiration is stored in Amazon DynamoDB as milliseconds. This results in a bug where keys are
    not automatically deleted because DynamoDB expects the TTL to be stored in seconds. As a
    one-time action, we will delete these keys from the table after February 21, 2018.

     **da2** : This version was introduced in February 2018 when AppSync added support to extend key
     expiration.

    * ``ListApiKeys`` returns the expiration time in seconds.

    * ``CreateApiKey`` returns the expiration time in seconds and accepts a user-provided expiration
    time in seconds.

    * ``UpdateApiKey`` returns the expiration time in seconds and accepts a user-provided expiration
    time in seconds. Key expiration can only be updated while the key has not expired.

    * ``DeleteApiKey`` deletes the item from the table.

    * Expiration is stored in Amazon DynamoDB as seconds.

    - **id** *(string) --*

      The API key ID.

    - **description** *(string) --*

      A description of the purpose of the API key.

    - **expires** *(integer) --*

      The time after which the API key expires. The date is represented as seconds since the epoch,
      rounded down to the nearest hour.
    """


_ListApiKeysPaginateResponseTypeDef = TypedDict(
    "_ListApiKeysPaginateResponseTypeDef",
    {"apiKeys": List[ListApiKeysPaginateResponseapiKeysTypeDef], "NextToken": str},
    total=False,
)


class ListApiKeysPaginateResponseTypeDef(_ListApiKeysPaginateResponseTypeDef):
    """
    Type definition for `ListApiKeysPaginate` `Response`

    - **apiKeys** *(list) --*

      The ``ApiKey`` objects.

      - *(dict) --*

        Describes an API key.

        Customers invoke AWS AppSync GraphQL API operations with API keys as an identity mechanism.
        There are two key versions:

         **da1** : This version was introduced at launch in November 2017. These keys always expire
         after 7 days. Key expiration is managed by Amazon DynamoDB TTL. The keys ceased to be valid
         after February 21, 2018 and should not be used after that date.

        * ``ListApiKeys`` returns the expiration time in milliseconds.

        * ``CreateApiKey`` returns the expiration time in milliseconds.

        * ``UpdateApiKey`` is not available for this key version.

        * ``DeleteApiKey`` deletes the item from the table.

        * Expiration is stored in Amazon DynamoDB as milliseconds. This results in a bug where keys
        are not automatically deleted because DynamoDB expects the TTL to be stored in seconds. As a
        one-time action, we will delete these keys from the table after February 21, 2018.

         **da2** : This version was introduced in February 2018 when AppSync added support to extend
         key expiration.

        * ``ListApiKeys`` returns the expiration time in seconds.

        * ``CreateApiKey`` returns the expiration time in seconds and accepts a user-provided
        expiration time in seconds.

        * ``UpdateApiKey`` returns the expiration time in seconds and accepts a user-provided
        expiration time in seconds. Key expiration can only be updated while the key has not
        expired.

        * ``DeleteApiKey`` deletes the item from the table.

        * Expiration is stored in Amazon DynamoDB as seconds.

        - **id** *(string) --*

          The API key ID.

        - **description** *(string) --*

          A description of the purpose of the API key.

        - **expires** *(integer) --*

          The time after which the API key expires. The date is represented as seconds since the
          epoch, rounded down to the nearest hour.

    - **NextToken** *(string) --*

      A token to resume pagination.
    """


_ListDataSourcesPaginatePaginationConfigTypeDef = TypedDict(
    "_ListDataSourcesPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class ListDataSourcesPaginatePaginationConfigTypeDef(
    _ListDataSourcesPaginatePaginationConfigTypeDef
):
    """
    Type definition for `ListDataSourcesPaginate` `PaginationConfig`

    A dictionary that provides parameters to control pagination.

    - **MaxItems** *(integer) --*

      The total number of items to return. If the total number of items available is more than the
      value specified in max-items then a ``NextToken`` will be provided in the output that you can
      use to resume pagination.

    - **PageSize** *(integer) --*

      The size of each page.

    - **StartingToken** *(string) --*

      A token to specify where to start paginating. This is the ``NextToken`` from a previous
      response.
    """


_ListDataSourcesPaginateResponsedataSourcesdynamodbConfigdeltaSyncConfigTypeDef = TypedDict(
    "_ListDataSourcesPaginateResponsedataSourcesdynamodbConfigdeltaSyncConfigTypeDef",
    {"baseTableTTL": int, "deltaSyncTableName": str, "deltaSyncTableTTL": int},
    total=False,
)


class ListDataSourcesPaginateResponsedataSourcesdynamodbConfigdeltaSyncConfigTypeDef(
    _ListDataSourcesPaginateResponsedataSourcesdynamodbConfigdeltaSyncConfigTypeDef
):
    """
    Type definition for `ListDataSourcesPaginateResponsedataSourcesdynamodbConfig` `deltaSyncConfig`

    The ``DeltaSyncConfig`` for a versioned datasource.

    - **baseTableTTL** *(integer) --*

      The number of minutes an Item is stored in the datasource.

    - **deltaSyncTableName** *(string) --*

      The Delta Sync table name.

    - **deltaSyncTableTTL** *(integer) --*

      The number of minutes a Delta Sync log entry is stored in the Delta Sync table.
    """


_ListDataSourcesPaginateResponsedataSourcesdynamodbConfigTypeDef = TypedDict(
    "_ListDataSourcesPaginateResponsedataSourcesdynamodbConfigTypeDef",
    {
        "tableName": str,
        "awsRegion": str,
        "useCallerCredentials": bool,
        "deltaSyncConfig": ListDataSourcesPaginateResponsedataSourcesdynamodbConfigdeltaSyncConfigTypeDef,
        "versioned": bool,
    },
    total=False,
)


class ListDataSourcesPaginateResponsedataSourcesdynamodbConfigTypeDef(
    _ListDataSourcesPaginateResponsedataSourcesdynamodbConfigTypeDef
):
    """
    Type definition for `ListDataSourcesPaginateResponsedataSources` `dynamodbConfig`

    Amazon DynamoDB settings.

    - **tableName** *(string) --*

      The table name.

    - **awsRegion** *(string) --*

      The AWS Region.

    - **useCallerCredentials** *(boolean) --*

      Set to TRUE to use Amazon Cognito credentials with this data source.

    - **deltaSyncConfig** *(dict) --*

      The ``DeltaSyncConfig`` for a versioned datasource.

      - **baseTableTTL** *(integer) --*

        The number of minutes an Item is stored in the datasource.

      - **deltaSyncTableName** *(string) --*

        The Delta Sync table name.

      - **deltaSyncTableTTL** *(integer) --*

        The number of minutes a Delta Sync log entry is stored in the Delta Sync table.

    - **versioned** *(boolean) --*

      Set to TRUE to use Conflict Detection and Resolution with this data source.
    """


_ListDataSourcesPaginateResponsedataSourceselasticsearchConfigTypeDef = TypedDict(
    "_ListDataSourcesPaginateResponsedataSourceselasticsearchConfigTypeDef",
    {"endpoint": str, "awsRegion": str},
    total=False,
)


class ListDataSourcesPaginateResponsedataSourceselasticsearchConfigTypeDef(
    _ListDataSourcesPaginateResponsedataSourceselasticsearchConfigTypeDef
):
    """
    Type definition for `ListDataSourcesPaginateResponsedataSources` `elasticsearchConfig`

    Amazon Elasticsearch Service settings.

    - **endpoint** *(string) --*

      The endpoint.

    - **awsRegion** *(string) --*

      The AWS Region.
    """


_ListDataSourcesPaginateResponsedataSourceshttpConfigauthorizationConfigawsIamConfigTypeDef = TypedDict(
    "_ListDataSourcesPaginateResponsedataSourceshttpConfigauthorizationConfigawsIamConfigTypeDef",
    {"signingRegion": str, "signingServiceName": str},
    total=False,
)


class ListDataSourcesPaginateResponsedataSourceshttpConfigauthorizationConfigawsIamConfigTypeDef(
    _ListDataSourcesPaginateResponsedataSourceshttpConfigauthorizationConfigawsIamConfigTypeDef
):
    """
    Type definition for `ListDataSourcesPaginateResponsedataSourceshttpConfigauthorizationConfig`
    `awsIamConfig`

    The AWS IAM settings.

    - **signingRegion** *(string) --*

      The signing region for AWS IAM authorization.

    - **signingServiceName** *(string) --*

      The signing service name for AWS IAM authorization.
    """


_ListDataSourcesPaginateResponsedataSourceshttpConfigauthorizationConfigTypeDef = TypedDict(
    "_ListDataSourcesPaginateResponsedataSourceshttpConfigauthorizationConfigTypeDef",
    {
        "authorizationType": str,
        "awsIamConfig": ListDataSourcesPaginateResponsedataSourceshttpConfigauthorizationConfigawsIamConfigTypeDef,
    },
    total=False,
)


class ListDataSourcesPaginateResponsedataSourceshttpConfigauthorizationConfigTypeDef(
    _ListDataSourcesPaginateResponsedataSourceshttpConfigauthorizationConfigTypeDef
):
    """
    Type definition for `ListDataSourcesPaginateResponsedataSourceshttpConfig` `authorizationConfig`

    The authorization config in case the HTTP endpoint requires authorization.

    - **authorizationType** *(string) --*

      The authorization type required by the HTTP endpoint.

      * **AWS_IAM** : The authorization type is Sigv4.

    - **awsIamConfig** *(dict) --*

      The AWS IAM settings.

      - **signingRegion** *(string) --*

        The signing region for AWS IAM authorization.

      - **signingServiceName** *(string) --*

        The signing service name for AWS IAM authorization.
    """


_ListDataSourcesPaginateResponsedataSourceshttpConfigTypeDef = TypedDict(
    "_ListDataSourcesPaginateResponsedataSourceshttpConfigTypeDef",
    {
        "endpoint": str,
        "authorizationConfig": ListDataSourcesPaginateResponsedataSourceshttpConfigauthorizationConfigTypeDef,
    },
    total=False,
)


class ListDataSourcesPaginateResponsedataSourceshttpConfigTypeDef(
    _ListDataSourcesPaginateResponsedataSourceshttpConfigTypeDef
):
    """
    Type definition for `ListDataSourcesPaginateResponsedataSources` `httpConfig`

    HTTP endpoint settings.

    - **endpoint** *(string) --*

      The HTTP URL endpoint. You can either specify the domain name or IP, and port combination, and
      the URL scheme must be HTTP or HTTPS. If the port is not specified, AWS AppSync uses the
      default port 80 for the HTTP endpoint and port 443 for HTTPS endpoints.

    - **authorizationConfig** *(dict) --*

      The authorization config in case the HTTP endpoint requires authorization.

      - **authorizationType** *(string) --*

        The authorization type required by the HTTP endpoint.

        * **AWS_IAM** : The authorization type is Sigv4.

      - **awsIamConfig** *(dict) --*

        The AWS IAM settings.

        - **signingRegion** *(string) --*

          The signing region for AWS IAM authorization.

        - **signingServiceName** *(string) --*

          The signing service name for AWS IAM authorization.
    """


_ListDataSourcesPaginateResponsedataSourceslambdaConfigTypeDef = TypedDict(
    "_ListDataSourcesPaginateResponsedataSourceslambdaConfigTypeDef",
    {"lambdaFunctionArn": str},
    total=False,
)


class ListDataSourcesPaginateResponsedataSourceslambdaConfigTypeDef(
    _ListDataSourcesPaginateResponsedataSourceslambdaConfigTypeDef
):
    """
    Type definition for `ListDataSourcesPaginateResponsedataSources` `lambdaConfig`

    AWS Lambda settings.

    - **lambdaFunctionArn** *(string) --*

      The ARN for the Lambda function.
    """


_ListDataSourcesPaginateResponsedataSourcesrelationalDatabaseConfigrdsHttpEndpointConfigTypeDef = TypedDict(
    "_ListDataSourcesPaginateResponsedataSourcesrelationalDatabaseConfigrdsHttpEndpointConfigTypeDef",
    {
        "awsRegion": str,
        "dbClusterIdentifier": str,
        "databaseName": str,
        "schema": str,
        "awsSecretStoreArn": str,
    },
    total=False,
)


class ListDataSourcesPaginateResponsedataSourcesrelationalDatabaseConfigrdsHttpEndpointConfigTypeDef(
    _ListDataSourcesPaginateResponsedataSourcesrelationalDatabaseConfigrdsHttpEndpointConfigTypeDef
):
    """
    Type definition for `ListDataSourcesPaginateResponsedataSourcesrelationalDatabaseConfig`
    `rdsHttpEndpointConfig`

    Amazon RDS HTTP endpoint settings.

    - **awsRegion** *(string) --*

      AWS Region for RDS HTTP endpoint.

    - **dbClusterIdentifier** *(string) --*

      Amazon RDS cluster identifier.

    - **databaseName** *(string) --*

      Logical database name.

    - **schema** *(string) --*

      Logical schema name.

    - **awsSecretStoreArn** *(string) --*

      AWS secret store ARN for database credentials.
    """


_ListDataSourcesPaginateResponsedataSourcesrelationalDatabaseConfigTypeDef = TypedDict(
    "_ListDataSourcesPaginateResponsedataSourcesrelationalDatabaseConfigTypeDef",
    {
        "relationalDatabaseSourceType": str,
        "rdsHttpEndpointConfig": ListDataSourcesPaginateResponsedataSourcesrelationalDatabaseConfigrdsHttpEndpointConfigTypeDef,
    },
    total=False,
)


class ListDataSourcesPaginateResponsedataSourcesrelationalDatabaseConfigTypeDef(
    _ListDataSourcesPaginateResponsedataSourcesrelationalDatabaseConfigTypeDef
):
    """
    Type definition for `ListDataSourcesPaginateResponsedataSources` `relationalDatabaseConfig`

    Relational database settings.

    - **relationalDatabaseSourceType** *(string) --*

      Source type for the relational database.

      * **RDS_HTTP_ENDPOINT** : The relational database source type is an Amazon RDS HTTP endpoint.

    - **rdsHttpEndpointConfig** *(dict) --*

      Amazon RDS HTTP endpoint settings.

      - **awsRegion** *(string) --*

        AWS Region for RDS HTTP endpoint.

      - **dbClusterIdentifier** *(string) --*

        Amazon RDS cluster identifier.

      - **databaseName** *(string) --*

        Logical database name.

      - **schema** *(string) --*

        Logical schema name.

      - **awsSecretStoreArn** *(string) --*

        AWS secret store ARN for database credentials.
    """


_ListDataSourcesPaginateResponsedataSourcesTypeDef = TypedDict(
    "_ListDataSourcesPaginateResponsedataSourcesTypeDef",
    {
        "dataSourceArn": str,
        "name": str,
        "description": str,
        "type": str,
        "serviceRoleArn": str,
        "dynamodbConfig": ListDataSourcesPaginateResponsedataSourcesdynamodbConfigTypeDef,
        "lambdaConfig": ListDataSourcesPaginateResponsedataSourceslambdaConfigTypeDef,
        "elasticsearchConfig": ListDataSourcesPaginateResponsedataSourceselasticsearchConfigTypeDef,
        "httpConfig": ListDataSourcesPaginateResponsedataSourceshttpConfigTypeDef,
        "relationalDatabaseConfig": ListDataSourcesPaginateResponsedataSourcesrelationalDatabaseConfigTypeDef,
    },
    total=False,
)


class ListDataSourcesPaginateResponsedataSourcesTypeDef(
    _ListDataSourcesPaginateResponsedataSourcesTypeDef
):
    """
    Type definition for `ListDataSourcesPaginateResponse` `dataSources`

    Describes a data source.

    - **dataSourceArn** *(string) --*

      The data source ARN.

    - **name** *(string) --*

      The name of the data source.

    - **description** *(string) --*

      The description of the data source.

    - **type** *(string) --*

      The type of the data source.

      * **AMAZON_DYNAMODB** : The data source is an Amazon DynamoDB table.

      * **AMAZON_ELASTICSEARCH** : The data source is an Amazon Elasticsearch Service domain.

      * **AWS_LAMBDA** : The data source is an AWS Lambda function.

      * **NONE** : There is no data source. This type is used when you wish to invoke a GraphQL
      operation without connecting to a data source, such as performing data transformation with
      resolvers or triggering a subscription to be invoked from a mutation.

      * **HTTP** : The data source is an HTTP endpoint.

      * **RELATIONAL_DATABASE** : The data source is a relational database.

    - **serviceRoleArn** *(string) --*

      The AWS IAM service role ARN for the data source. The system assumes this role when accessing
      the data source.

    - **dynamodbConfig** *(dict) --*

      Amazon DynamoDB settings.

      - **tableName** *(string) --*

        The table name.

      - **awsRegion** *(string) --*

        The AWS Region.

      - **useCallerCredentials** *(boolean) --*

        Set to TRUE to use Amazon Cognito credentials with this data source.

      - **deltaSyncConfig** *(dict) --*

        The ``DeltaSyncConfig`` for a versioned datasource.

        - **baseTableTTL** *(integer) --*

          The number of minutes an Item is stored in the datasource.

        - **deltaSyncTableName** *(string) --*

          The Delta Sync table name.

        - **deltaSyncTableTTL** *(integer) --*

          The number of minutes a Delta Sync log entry is stored in the Delta Sync table.

      - **versioned** *(boolean) --*

        Set to TRUE to use Conflict Detection and Resolution with this data source.

    - **lambdaConfig** *(dict) --*

      AWS Lambda settings.

      - **lambdaFunctionArn** *(string) --*

        The ARN for the Lambda function.

    - **elasticsearchConfig** *(dict) --*

      Amazon Elasticsearch Service settings.

      - **endpoint** *(string) --*

        The endpoint.

      - **awsRegion** *(string) --*

        The AWS Region.

    - **httpConfig** *(dict) --*

      HTTP endpoint settings.

      - **endpoint** *(string) --*

        The HTTP URL endpoint. You can either specify the domain name or IP, and port combination,
        and the URL scheme must be HTTP or HTTPS. If the port is not specified, AWS AppSync uses the
        default port 80 for the HTTP endpoint and port 443 for HTTPS endpoints.

      - **authorizationConfig** *(dict) --*

        The authorization config in case the HTTP endpoint requires authorization.

        - **authorizationType** *(string) --*

          The authorization type required by the HTTP endpoint.

          * **AWS_IAM** : The authorization type is Sigv4.

        - **awsIamConfig** *(dict) --*

          The AWS IAM settings.

          - **signingRegion** *(string) --*

            The signing region for AWS IAM authorization.

          - **signingServiceName** *(string) --*

            The signing service name for AWS IAM authorization.

    - **relationalDatabaseConfig** *(dict) --*

      Relational database settings.

      - **relationalDatabaseSourceType** *(string) --*

        Source type for the relational database.

        * **RDS_HTTP_ENDPOINT** : The relational database source type is an Amazon RDS HTTP
        endpoint.

      - **rdsHttpEndpointConfig** *(dict) --*

        Amazon RDS HTTP endpoint settings.

        - **awsRegion** *(string) --*

          AWS Region for RDS HTTP endpoint.

        - **dbClusterIdentifier** *(string) --*

          Amazon RDS cluster identifier.

        - **databaseName** *(string) --*

          Logical database name.

        - **schema** *(string) --*

          Logical schema name.

        - **awsSecretStoreArn** *(string) --*

          AWS secret store ARN for database credentials.
    """


_ListDataSourcesPaginateResponseTypeDef = TypedDict(
    "_ListDataSourcesPaginateResponseTypeDef",
    {"dataSources": List[ListDataSourcesPaginateResponsedataSourcesTypeDef], "NextToken": str},
    total=False,
)


class ListDataSourcesPaginateResponseTypeDef(_ListDataSourcesPaginateResponseTypeDef):
    """
    Type definition for `ListDataSourcesPaginate` `Response`

    - **dataSources** *(list) --*

      The ``DataSource`` objects.

      - *(dict) --*

        Describes a data source.

        - **dataSourceArn** *(string) --*

          The data source ARN.

        - **name** *(string) --*

          The name of the data source.

        - **description** *(string) --*

          The description of the data source.

        - **type** *(string) --*

          The type of the data source.

          * **AMAZON_DYNAMODB** : The data source is an Amazon DynamoDB table.

          * **AMAZON_ELASTICSEARCH** : The data source is an Amazon Elasticsearch Service domain.

          * **AWS_LAMBDA** : The data source is an AWS Lambda function.

          * **NONE** : There is no data source. This type is used when you wish to invoke a GraphQL
          operation without connecting to a data source, such as performing data transformation with
          resolvers or triggering a subscription to be invoked from a mutation.

          * **HTTP** : The data source is an HTTP endpoint.

          * **RELATIONAL_DATABASE** : The data source is a relational database.

        - **serviceRoleArn** *(string) --*

          The AWS IAM service role ARN for the data source. The system assumes this role when
          accessing the data source.

        - **dynamodbConfig** *(dict) --*

          Amazon DynamoDB settings.

          - **tableName** *(string) --*

            The table name.

          - **awsRegion** *(string) --*

            The AWS Region.

          - **useCallerCredentials** *(boolean) --*

            Set to TRUE to use Amazon Cognito credentials with this data source.

          - **deltaSyncConfig** *(dict) --*

            The ``DeltaSyncConfig`` for a versioned datasource.

            - **baseTableTTL** *(integer) --*

              The number of minutes an Item is stored in the datasource.

            - **deltaSyncTableName** *(string) --*

              The Delta Sync table name.

            - **deltaSyncTableTTL** *(integer) --*

              The number of minutes a Delta Sync log entry is stored in the Delta Sync table.

          - **versioned** *(boolean) --*

            Set to TRUE to use Conflict Detection and Resolution with this data source.

        - **lambdaConfig** *(dict) --*

          AWS Lambda settings.

          - **lambdaFunctionArn** *(string) --*

            The ARN for the Lambda function.

        - **elasticsearchConfig** *(dict) --*

          Amazon Elasticsearch Service settings.

          - **endpoint** *(string) --*

            The endpoint.

          - **awsRegion** *(string) --*

            The AWS Region.

        - **httpConfig** *(dict) --*

          HTTP endpoint settings.

          - **endpoint** *(string) --*

            The HTTP URL endpoint. You can either specify the domain name or IP, and port
            combination, and the URL scheme must be HTTP or HTTPS. If the port is not specified, AWS
            AppSync uses the default port 80 for the HTTP endpoint and port 443 for HTTPS endpoints.

          - **authorizationConfig** *(dict) --*

            The authorization config in case the HTTP endpoint requires authorization.

            - **authorizationType** *(string) --*

              The authorization type required by the HTTP endpoint.

              * **AWS_IAM** : The authorization type is Sigv4.

            - **awsIamConfig** *(dict) --*

              The AWS IAM settings.

              - **signingRegion** *(string) --*

                The signing region for AWS IAM authorization.

              - **signingServiceName** *(string) --*

                The signing service name for AWS IAM authorization.

        - **relationalDatabaseConfig** *(dict) --*

          Relational database settings.

          - **relationalDatabaseSourceType** *(string) --*

            Source type for the relational database.

            * **RDS_HTTP_ENDPOINT** : The relational database source type is an Amazon RDS HTTP
            endpoint.

          - **rdsHttpEndpointConfig** *(dict) --*

            Amazon RDS HTTP endpoint settings.

            - **awsRegion** *(string) --*

              AWS Region for RDS HTTP endpoint.

            - **dbClusterIdentifier** *(string) --*

              Amazon RDS cluster identifier.

            - **databaseName** *(string) --*

              Logical database name.

            - **schema** *(string) --*

              Logical schema name.

            - **awsSecretStoreArn** *(string) --*

              AWS secret store ARN for database credentials.

    - **NextToken** *(string) --*

      A token to resume pagination.
    """


_ListFunctionsPaginatePaginationConfigTypeDef = TypedDict(
    "_ListFunctionsPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class ListFunctionsPaginatePaginationConfigTypeDef(_ListFunctionsPaginatePaginationConfigTypeDef):
    """
    Type definition for `ListFunctionsPaginate` `PaginationConfig`

    A dictionary that provides parameters to control pagination.

    - **MaxItems** *(integer) --*

      The total number of items to return. If the total number of items available is more than the
      value specified in max-items then a ``NextToken`` will be provided in the output that you can
      use to resume pagination.

    - **PageSize** *(integer) --*

      The size of each page.

    - **StartingToken** *(string) --*

      A token to specify where to start paginating. This is the ``NextToken`` from a previous
      response.
    """


_ListFunctionsPaginateResponsefunctionsTypeDef = TypedDict(
    "_ListFunctionsPaginateResponsefunctionsTypeDef",
    {
        "functionId": str,
        "functionArn": str,
        "name": str,
        "description": str,
        "dataSourceName": str,
        "requestMappingTemplate": str,
        "responseMappingTemplate": str,
        "functionVersion": str,
    },
    total=False,
)


class ListFunctionsPaginateResponsefunctionsTypeDef(_ListFunctionsPaginateResponsefunctionsTypeDef):
    """
    Type definition for `ListFunctionsPaginateResponse` `functions`

    A function is a reusable entity. Multiple functions can be used to compose the resolver logic.

    - **functionId** *(string) --*

      A unique ID representing the ``Function`` object.

    - **functionArn** *(string) --*

      The ARN of the ``Function`` object.

    - **name** *(string) --*

      The name of the ``Function`` object.

    - **description** *(string) --*

      The ``Function`` description.

    - **dataSourceName** *(string) --*

      The name of the ``DataSource`` .

    - **requestMappingTemplate** *(string) --*

      The ``Function`` request mapping template. Functions support only the 2018-05-29 version of
      the request mapping template.

    - **responseMappingTemplate** *(string) --*

      The ``Function`` response mapping template.

    - **functionVersion** *(string) --*

      The version of the request mapping template. Currently only the 2018-05-29 version of the
      template is supported.
    """


_ListFunctionsPaginateResponseTypeDef = TypedDict(
    "_ListFunctionsPaginateResponseTypeDef",
    {"functions": List[ListFunctionsPaginateResponsefunctionsTypeDef], "NextToken": str},
    total=False,
)


class ListFunctionsPaginateResponseTypeDef(_ListFunctionsPaginateResponseTypeDef):
    """
    Type definition for `ListFunctionsPaginate` `Response`

    - **functions** *(list) --*

      A list of ``Function`` objects.

      - *(dict) --*

        A function is a reusable entity. Multiple functions can be used to compose the resolver
        logic.

        - **functionId** *(string) --*

          A unique ID representing the ``Function`` object.

        - **functionArn** *(string) --*

          The ARN of the ``Function`` object.

        - **name** *(string) --*

          The name of the ``Function`` object.

        - **description** *(string) --*

          The ``Function`` description.

        - **dataSourceName** *(string) --*

          The name of the ``DataSource`` .

        - **requestMappingTemplate** *(string) --*

          The ``Function`` request mapping template. Functions support only the 2018-05-29 version
          of the request mapping template.

        - **responseMappingTemplate** *(string) --*

          The ``Function`` response mapping template.

        - **functionVersion** *(string) --*

          The version of the request mapping template. Currently only the 2018-05-29 version of the
          template is supported.

    - **NextToken** *(string) --*

      A token to resume pagination.
    """


_ListGraphqlApisPaginatePaginationConfigTypeDef = TypedDict(
    "_ListGraphqlApisPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class ListGraphqlApisPaginatePaginationConfigTypeDef(
    _ListGraphqlApisPaginatePaginationConfigTypeDef
):
    """
    Type definition for `ListGraphqlApisPaginate` `PaginationConfig`

    A dictionary that provides parameters to control pagination.

    - **MaxItems** *(integer) --*

      The total number of items to return. If the total number of items available is more than the
      value specified in max-items then a ``NextToken`` will be provided in the output that you can
      use to resume pagination.

    - **PageSize** *(integer) --*

      The size of each page.

    - **StartingToken** *(string) --*

      A token to specify where to start paginating. This is the ``NextToken`` from a previous
      response.
    """


_ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProvidersopenIDConnectConfigTypeDef = TypedDict(
    "_ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProvidersopenIDConnectConfigTypeDef",
    {"issuer": str, "clientId": str, "iatTTL": int, "authTTL": int},
    total=False,
)


class ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProvidersopenIDConnectConfigTypeDef(
    _ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProvidersopenIDConnectConfigTypeDef
):
    """
    Type definition for
    `ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProviders`
    `openIDConnectConfig`

    The OpenID Connect configuration.

    - **issuer** *(string) --*

      The issuer for the OpenID Connect configuration. The issuer returned by discovery must exactly
      match the value of ``iss`` in the ID token.

    - **clientId** *(string) --*

      The client identifier of the Relying party at the OpenID identity provider. This identifier is
      typically obtained when the Relying party is registered with the OpenID identity provider. You
      can specify a regular expression so the AWS AppSync can validate against multiple client
      identifiers at a time.

    - **iatTTL** *(integer) --*

      The number of milliseconds a token is valid after being issued to a user.

    - **authTTL** *(integer) --*

      The number of milliseconds a token is valid after being authenticated.
    """


_ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProvidersuserPoolConfigTypeDef = TypedDict(
    "_ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProvidersuserPoolConfigTypeDef",
    {"userPoolId": str, "awsRegion": str, "appIdClientRegex": str},
    total=False,
)


class ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProvidersuserPoolConfigTypeDef(
    _ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProvidersuserPoolConfigTypeDef
):
    """
    Type definition for
    `ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProviders` `userPoolConfig`

    The Amazon Cognito user pool configuration.

    - **userPoolId** *(string) --*

      The user pool ID.

    - **awsRegion** *(string) --*

      The AWS Region in which the user pool was created.

    - **appIdClientRegex** *(string) --*

      A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProvidersTypeDef = TypedDict(
    "_ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProvidersTypeDef",
    {
        "authenticationType": str,
        "openIDConnectConfig": ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProvidersopenIDConnectConfigTypeDef,
        "userPoolConfig": ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProvidersuserPoolConfigTypeDef,
    },
    total=False,
)


class ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProvidersTypeDef(
    _ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProvidersTypeDef
):
    """
    Type definition for `ListGraphqlApisPaginateResponsegraphqlApis`
    `additionalAuthenticationProviders`

    Describes an additional authentication provider.

    - **authenticationType** *(string) --*

      The authentication type: API key, AWS IAM, OIDC, or Amazon Cognito user pools.

    - **openIDConnectConfig** *(dict) --*

      The OpenID Connect configuration.

      - **issuer** *(string) --*

        The issuer for the OpenID Connect configuration. The issuer returned by discovery must
        exactly match the value of ``iss`` in the ID token.

      - **clientId** *(string) --*

        The client identifier of the Relying party at the OpenID identity provider. This identifier
        is typically obtained when the Relying party is registered with the OpenID identity
        provider. You can specify a regular expression so the AWS AppSync can validate against
        multiple client identifiers at a time.

      - **iatTTL** *(integer) --*

        The number of milliseconds a token is valid after being issued to a user.

      - **authTTL** *(integer) --*

        The number of milliseconds a token is valid after being authenticated.

    - **userPoolConfig** *(dict) --*

      The Amazon Cognito user pool configuration.

      - **userPoolId** *(string) --*

        The user pool ID.

      - **awsRegion** *(string) --*

        The AWS Region in which the user pool was created.

      - **appIdClientRegex** *(string) --*

        A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ListGraphqlApisPaginateResponsegraphqlApislogConfigTypeDef = TypedDict(
    "_ListGraphqlApisPaginateResponsegraphqlApislogConfigTypeDef",
    {"fieldLogLevel": str, "cloudWatchLogsRoleArn": str, "excludeVerboseContent": bool},
    total=False,
)


class ListGraphqlApisPaginateResponsegraphqlApislogConfigTypeDef(
    _ListGraphqlApisPaginateResponsegraphqlApislogConfigTypeDef
):
    """
    Type definition for `ListGraphqlApisPaginateResponsegraphqlApis` `logConfig`

    The Amazon CloudWatch Logs configuration.

    - **fieldLogLevel** *(string) --*

      The field logging level. Values can be NONE, ERROR, or ALL.

      * **NONE** : No field-level logs are captured.

      * **ERROR** : Logs the following information only for the fields that are in error:

        * The error section in the server response.

        * Field-level errors.

        * The generated request/response functions that got resolved for error fields.

      * **ALL** : The following information is logged for all fields in the query:

        * Field-level tracing information.

        * The generated request/response functions that got resolved for each field.

    - **cloudWatchLogsRoleArn** *(string) --*

      The service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in your
      account.

    - **excludeVerboseContent** *(boolean) --*

      Set to TRUE to exclude sections that contain information such as headers, context, and
      evaluated mapping templates, regardless of logging level.
    """


_ListGraphqlApisPaginateResponsegraphqlApisopenIDConnectConfigTypeDef = TypedDict(
    "_ListGraphqlApisPaginateResponsegraphqlApisopenIDConnectConfigTypeDef",
    {"issuer": str, "clientId": str, "iatTTL": int, "authTTL": int},
    total=False,
)


class ListGraphqlApisPaginateResponsegraphqlApisopenIDConnectConfigTypeDef(
    _ListGraphqlApisPaginateResponsegraphqlApisopenIDConnectConfigTypeDef
):
    """
    Type definition for `ListGraphqlApisPaginateResponsegraphqlApis` `openIDConnectConfig`

    The OpenID Connect configuration.

    - **issuer** *(string) --*

      The issuer for the OpenID Connect configuration. The issuer returned by discovery must exactly
      match the value of ``iss`` in the ID token.

    - **clientId** *(string) --*

      The client identifier of the Relying party at the OpenID identity provider. This identifier is
      typically obtained when the Relying party is registered with the OpenID identity provider. You
      can specify a regular expression so the AWS AppSync can validate against multiple client
      identifiers at a time.

    - **iatTTL** *(integer) --*

      The number of milliseconds a token is valid after being issued to a user.

    - **authTTL** *(integer) --*

      The number of milliseconds a token is valid after being authenticated.
    """


_ListGraphqlApisPaginateResponsegraphqlApisuserPoolConfigTypeDef = TypedDict(
    "_ListGraphqlApisPaginateResponsegraphqlApisuserPoolConfigTypeDef",
    {"userPoolId": str, "awsRegion": str, "defaultAction": str, "appIdClientRegex": str},
    total=False,
)


class ListGraphqlApisPaginateResponsegraphqlApisuserPoolConfigTypeDef(
    _ListGraphqlApisPaginateResponsegraphqlApisuserPoolConfigTypeDef
):
    """
    Type definition for `ListGraphqlApisPaginateResponsegraphqlApis` `userPoolConfig`

    The Amazon Cognito user pool configuration.

    - **userPoolId** *(string) --*

      The user pool ID.

    - **awsRegion** *(string) --*

      The AWS Region in which the user pool was created.

    - **defaultAction** *(string) --*

      The action that you want your GraphQL API to take when a request that uses Amazon Cognito user
      pool authentication doesn't match the Amazon Cognito user pool configuration.

    - **appIdClientRegex** *(string) --*

      A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ListGraphqlApisPaginateResponsegraphqlApisTypeDef = TypedDict(
    "_ListGraphqlApisPaginateResponsegraphqlApisTypeDef",
    {
        "name": str,
        "apiId": str,
        "authenticationType": str,
        "logConfig": ListGraphqlApisPaginateResponsegraphqlApislogConfigTypeDef,
        "userPoolConfig": ListGraphqlApisPaginateResponsegraphqlApisuserPoolConfigTypeDef,
        "openIDConnectConfig": ListGraphqlApisPaginateResponsegraphqlApisopenIDConnectConfigTypeDef,
        "arn": str,
        "uris": Dict[str, str],
        "tags": Dict[str, str],
        "additionalAuthenticationProviders": List[
            ListGraphqlApisPaginateResponsegraphqlApisadditionalAuthenticationProvidersTypeDef
        ],
    },
    total=False,
)


class ListGraphqlApisPaginateResponsegraphqlApisTypeDef(
    _ListGraphqlApisPaginateResponsegraphqlApisTypeDef
):
    """
    Type definition for `ListGraphqlApisPaginateResponse` `graphqlApis`

    Describes a GraphQL API.

    - **name** *(string) --*

      The API name.

    - **apiId** *(string) --*

      The API ID.

    - **authenticationType** *(string) --*

      The authentication type.

    - **logConfig** *(dict) --*

      The Amazon CloudWatch Logs configuration.

      - **fieldLogLevel** *(string) --*

        The field logging level. Values can be NONE, ERROR, or ALL.

        * **NONE** : No field-level logs are captured.

        * **ERROR** : Logs the following information only for the fields that are in error:

          * The error section in the server response.

          * Field-level errors.

          * The generated request/response functions that got resolved for error fields.

        * **ALL** : The following information is logged for all fields in the query:

          * Field-level tracing information.

          * The generated request/response functions that got resolved for each field.

      - **cloudWatchLogsRoleArn** *(string) --*

        The service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in your
        account.

      - **excludeVerboseContent** *(boolean) --*

        Set to TRUE to exclude sections that contain information such as headers, context, and
        evaluated mapping templates, regardless of logging level.

    - **userPoolConfig** *(dict) --*

      The Amazon Cognito user pool configuration.

      - **userPoolId** *(string) --*

        The user pool ID.

      - **awsRegion** *(string) --*

        The AWS Region in which the user pool was created.

      - **defaultAction** *(string) --*

        The action that you want your GraphQL API to take when a request that uses Amazon Cognito
        user pool authentication doesn't match the Amazon Cognito user pool configuration.

      - **appIdClientRegex** *(string) --*

        A regular expression for validating the incoming Amazon Cognito user pool app client ID.

    - **openIDConnectConfig** *(dict) --*

      The OpenID Connect configuration.

      - **issuer** *(string) --*

        The issuer for the OpenID Connect configuration. The issuer returned by discovery must
        exactly match the value of ``iss`` in the ID token.

      - **clientId** *(string) --*

        The client identifier of the Relying party at the OpenID identity provider. This identifier
        is typically obtained when the Relying party is registered with the OpenID identity
        provider. You can specify a regular expression so the AWS AppSync can validate against
        multiple client identifiers at a time.

      - **iatTTL** *(integer) --*

        The number of milliseconds a token is valid after being issued to a user.

      - **authTTL** *(integer) --*

        The number of milliseconds a token is valid after being authenticated.

    - **arn** *(string) --*

      The ARN.

    - **uris** *(dict) --*

      The URIs.

      - *(string) --*

        - *(string) --*

    - **tags** *(dict) --*

      The tags.

      - *(string) --*

        The key for the tag.

        - *(string) --*

          The value for the tag.

    - **additionalAuthenticationProviders** *(list) --*

      A list of additional authentication providers for the ``GraphqlApi`` API.

      - *(dict) --*

        Describes an additional authentication provider.

        - **authenticationType** *(string) --*

          The authentication type: API key, AWS IAM, OIDC, or Amazon Cognito user pools.

        - **openIDConnectConfig** *(dict) --*

          The OpenID Connect configuration.

          - **issuer** *(string) --*

            The issuer for the OpenID Connect configuration. The issuer returned by discovery must
            exactly match the value of ``iss`` in the ID token.

          - **clientId** *(string) --*

            The client identifier of the Relying party at the OpenID identity provider. This
            identifier is typically obtained when the Relying party is registered with the OpenID
            identity provider. You can specify a regular expression so the AWS AppSync can validate
            against multiple client identifiers at a time.

          - **iatTTL** *(integer) --*

            The number of milliseconds a token is valid after being issued to a user.

          - **authTTL** *(integer) --*

            The number of milliseconds a token is valid after being authenticated.

        - **userPoolConfig** *(dict) --*

          The Amazon Cognito user pool configuration.

          - **userPoolId** *(string) --*

            The user pool ID.

          - **awsRegion** *(string) --*

            The AWS Region in which the user pool was created.

          - **appIdClientRegex** *(string) --*

            A regular expression for validating the incoming Amazon Cognito user pool app client ID.
    """


_ListGraphqlApisPaginateResponseTypeDef = TypedDict(
    "_ListGraphqlApisPaginateResponseTypeDef",
    {"graphqlApis": List[ListGraphqlApisPaginateResponsegraphqlApisTypeDef], "NextToken": str},
    total=False,
)


class ListGraphqlApisPaginateResponseTypeDef(_ListGraphqlApisPaginateResponseTypeDef):
    """
    Type definition for `ListGraphqlApisPaginate` `Response`

    - **graphqlApis** *(list) --*

      The ``GraphqlApi`` objects.

      - *(dict) --*

        Describes a GraphQL API.

        - **name** *(string) --*

          The API name.

        - **apiId** *(string) --*

          The API ID.

        - **authenticationType** *(string) --*

          The authentication type.

        - **logConfig** *(dict) --*

          The Amazon CloudWatch Logs configuration.

          - **fieldLogLevel** *(string) --*

            The field logging level. Values can be NONE, ERROR, or ALL.

            * **NONE** : No field-level logs are captured.

            * **ERROR** : Logs the following information only for the fields that are in error:

              * The error section in the server response.

              * Field-level errors.

              * The generated request/response functions that got resolved for error fields.

            * **ALL** : The following information is logged for all fields in the query:

              * Field-level tracing information.

              * The generated request/response functions that got resolved for each field.

          - **cloudWatchLogsRoleArn** *(string) --*

            The service role that AWS AppSync will assume to publish to Amazon CloudWatch logs in
            your account.

          - **excludeVerboseContent** *(boolean) --*

            Set to TRUE to exclude sections that contain information such as headers, context, and
            evaluated mapping templates, regardless of logging level.

        - **userPoolConfig** *(dict) --*

          The Amazon Cognito user pool configuration.

          - **userPoolId** *(string) --*

            The user pool ID.

          - **awsRegion** *(string) --*

            The AWS Region in which the user pool was created.

          - **defaultAction** *(string) --*

            The action that you want your GraphQL API to take when a request that uses Amazon
            Cognito user pool authentication doesn't match the Amazon Cognito user pool
            configuration.

          - **appIdClientRegex** *(string) --*

            A regular expression for validating the incoming Amazon Cognito user pool app client ID.

        - **openIDConnectConfig** *(dict) --*

          The OpenID Connect configuration.

          - **issuer** *(string) --*

            The issuer for the OpenID Connect configuration. The issuer returned by discovery must
            exactly match the value of ``iss`` in the ID token.

          - **clientId** *(string) --*

            The client identifier of the Relying party at the OpenID identity provider. This
            identifier is typically obtained when the Relying party is registered with the OpenID
            identity provider. You can specify a regular expression so the AWS AppSync can validate
            against multiple client identifiers at a time.

          - **iatTTL** *(integer) --*

            The number of milliseconds a token is valid after being issued to a user.

          - **authTTL** *(integer) --*

            The number of milliseconds a token is valid after being authenticated.

        - **arn** *(string) --*

          The ARN.

        - **uris** *(dict) --*

          The URIs.

          - *(string) --*

            - *(string) --*

        - **tags** *(dict) --*

          The tags.

          - *(string) --*

            The key for the tag.

            - *(string) --*

              The value for the tag.

        - **additionalAuthenticationProviders** *(list) --*

          A list of additional authentication providers for the ``GraphqlApi`` API.

          - *(dict) --*

            Describes an additional authentication provider.

            - **authenticationType** *(string) --*

              The authentication type: API key, AWS IAM, OIDC, or Amazon Cognito user pools.

            - **openIDConnectConfig** *(dict) --*

              The OpenID Connect configuration.

              - **issuer** *(string) --*

                The issuer for the OpenID Connect configuration. The issuer returned by discovery
                must exactly match the value of ``iss`` in the ID token.

              - **clientId** *(string) --*

                The client identifier of the Relying party at the OpenID identity provider. This
                identifier is typically obtained when the Relying party is registered with the
                OpenID identity provider. You can specify a regular expression so the AWS AppSync
                can validate against multiple client identifiers at a time.

              - **iatTTL** *(integer) --*

                The number of milliseconds a token is valid after being issued to a user.

              - **authTTL** *(integer) --*

                The number of milliseconds a token is valid after being authenticated.

            - **userPoolConfig** *(dict) --*

              The Amazon Cognito user pool configuration.

              - **userPoolId** *(string) --*

                The user pool ID.

              - **awsRegion** *(string) --*

                The AWS Region in which the user pool was created.

              - **appIdClientRegex** *(string) --*

                A regular expression for validating the incoming Amazon Cognito user pool app client
                ID.

    - **NextToken** *(string) --*

      A token to resume pagination.
    """


_ListResolversByFunctionPaginatePaginationConfigTypeDef = TypedDict(
    "_ListResolversByFunctionPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class ListResolversByFunctionPaginatePaginationConfigTypeDef(
    _ListResolversByFunctionPaginatePaginationConfigTypeDef
):
    """
    Type definition for `ListResolversByFunctionPaginate` `PaginationConfig`

    A dictionary that provides parameters to control pagination.

    - **MaxItems** *(integer) --*

      The total number of items to return. If the total number of items available is more than the
      value specified in max-items then a ``NextToken`` will be provided in the output that you can
      use to resume pagination.

    - **PageSize** *(integer) --*

      The size of each page.

    - **StartingToken** *(string) --*

      A token to specify where to start paginating. This is the ``NextToken`` from a previous
      response.
    """


_ListResolversByFunctionPaginateResponseresolverscachingConfigTypeDef = TypedDict(
    "_ListResolversByFunctionPaginateResponseresolverscachingConfigTypeDef",
    {"ttl": int, "cachingKeys": List[str]},
    total=False,
)


class ListResolversByFunctionPaginateResponseresolverscachingConfigTypeDef(
    _ListResolversByFunctionPaginateResponseresolverscachingConfigTypeDef
):
    """
    Type definition for `ListResolversByFunctionPaginateResponseresolvers` `cachingConfig`

    The caching configuration for the resolver.

    - **ttl** *(integer) --*

      The TTL in seconds for a resolver that has caching enabled.

      Valid values are between 1 and 3600 seconds.

    - **cachingKeys** *(list) --*

      The caching keys for a resolver that has caching enabled.

      Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

      - *(string) --*
    """


_ListResolversByFunctionPaginateResponseresolverspipelineConfigTypeDef = TypedDict(
    "_ListResolversByFunctionPaginateResponseresolverspipelineConfigTypeDef",
    {"functions": List[str]},
    total=False,
)


class ListResolversByFunctionPaginateResponseresolverspipelineConfigTypeDef(
    _ListResolversByFunctionPaginateResponseresolverspipelineConfigTypeDef
):
    """
    Type definition for `ListResolversByFunctionPaginateResponseresolvers` `pipelineConfig`

    The ``PipelineConfig`` .

    - **functions** *(list) --*

      A list of ``Function`` objects.

      - *(string) --*
    """


_ListResolversByFunctionPaginateResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef = TypedDict(
    "_ListResolversByFunctionPaginateResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef",
    {"lambdaConflictHandlerArn": str},
    total=False,
)


class ListResolversByFunctionPaginateResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef(
    _ListResolversByFunctionPaginateResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef
):
    """
    Type definition for `ListResolversByFunctionPaginateResponseresolverssyncConfig`
    `lambdaConflictHandlerConfig`

    The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

    - **lambdaConflictHandlerArn** *(string) --*

      The Arn for the Lambda function to use as the Conflict Handler.
    """


_ListResolversByFunctionPaginateResponseresolverssyncConfigTypeDef = TypedDict(
    "_ListResolversByFunctionPaginateResponseresolverssyncConfigTypeDef",
    {
        "conflictHandler": str,
        "conflictDetection": str,
        "lambdaConflictHandlerConfig": ListResolversByFunctionPaginateResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef,
    },
    total=False,
)


class ListResolversByFunctionPaginateResponseresolverssyncConfigTypeDef(
    _ListResolversByFunctionPaginateResponseresolverssyncConfigTypeDef
):
    """
    Type definition for `ListResolversByFunctionPaginateResponseresolvers` `syncConfig`

    The ``SyncConfig`` for a resolver attached to a versioned datasource.

    - **conflictHandler** *(string) --*

      The Conflict Resolution strategy to perform in the event of a conflict.

      * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do not
      match the latest version at the server.

      * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

      * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
      LambdaConflictHandlerConfig.

    - **conflictDetection** *(string) --*

      The Conflict Detection strategy to use.

      * **VERSION** : Detect conflicts based on object versions for this resolver.

      * **NONE** : Do not detect conflicts when executing this resolver.

    - **lambdaConflictHandlerConfig** *(dict) --*

      The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

      - **lambdaConflictHandlerArn** *(string) --*

        The Arn for the Lambda function to use as the Conflict Handler.
    """


_ListResolversByFunctionPaginateResponseresolversTypeDef = TypedDict(
    "_ListResolversByFunctionPaginateResponseresolversTypeDef",
    {
        "typeName": str,
        "fieldName": str,
        "dataSourceName": str,
        "resolverArn": str,
        "requestMappingTemplate": str,
        "responseMappingTemplate": str,
        "kind": str,
        "pipelineConfig": ListResolversByFunctionPaginateResponseresolverspipelineConfigTypeDef,
        "syncConfig": ListResolversByFunctionPaginateResponseresolverssyncConfigTypeDef,
        "cachingConfig": ListResolversByFunctionPaginateResponseresolverscachingConfigTypeDef,
    },
    total=False,
)


class ListResolversByFunctionPaginateResponseresolversTypeDef(
    _ListResolversByFunctionPaginateResponseresolversTypeDef
):
    """
    Type definition for `ListResolversByFunctionPaginateResponse` `resolvers`

    Describes a resolver.

    - **typeName** *(string) --*

      The resolver type name.

    - **fieldName** *(string) --*

      The resolver field name.

    - **dataSourceName** *(string) --*

      The resolver data source name.

    - **resolverArn** *(string) --*

      The resolver ARN.

    - **requestMappingTemplate** *(string) --*

      The request mapping template.

    - **responseMappingTemplate** *(string) --*

      The response mapping template.

    - **kind** *(string) --*

      The resolver type.

      * **UNIT** : A UNIT resolver type. A UNIT resolver is the default resolver type. A UNIT
      resolver enables you to execute a GraphQL query against a single data source.

      * **PIPELINE** : A PIPELINE resolver type. A PIPELINE resolver enables you to execute a series
      of ``Function`` in a serial manner. You can use a pipeline resolver to execute a GraphQL query
      against multiple data sources.

    - **pipelineConfig** *(dict) --*

      The ``PipelineConfig`` .

      - **functions** *(list) --*

        A list of ``Function`` objects.

        - *(string) --*

    - **syncConfig** *(dict) --*

      The ``SyncConfig`` for a resolver attached to a versioned datasource.

      - **conflictHandler** *(string) --*

        The Conflict Resolution strategy to perform in the event of a conflict.

        * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do not
        match the latest version at the server.

        * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

        * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
        LambdaConflictHandlerConfig.

      - **conflictDetection** *(string) --*

        The Conflict Detection strategy to use.

        * **VERSION** : Detect conflicts based on object versions for this resolver.

        * **NONE** : Do not detect conflicts when executing this resolver.

      - **lambdaConflictHandlerConfig** *(dict) --*

        The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

        - **lambdaConflictHandlerArn** *(string) --*

          The Arn for the Lambda function to use as the Conflict Handler.

    - **cachingConfig** *(dict) --*

      The caching configuration for the resolver.

      - **ttl** *(integer) --*

        The TTL in seconds for a resolver that has caching enabled.

        Valid values are between 1 and 3600 seconds.

      - **cachingKeys** *(list) --*

        The caching keys for a resolver that has caching enabled.

        Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

        - *(string) --*
    """


_ListResolversByFunctionPaginateResponseTypeDef = TypedDict(
    "_ListResolversByFunctionPaginateResponseTypeDef",
    {"resolvers": List[ListResolversByFunctionPaginateResponseresolversTypeDef], "NextToken": str},
    total=False,
)


class ListResolversByFunctionPaginateResponseTypeDef(
    _ListResolversByFunctionPaginateResponseTypeDef
):
    """
    Type definition for `ListResolversByFunctionPaginate` `Response`

    - **resolvers** *(list) --*

      The list of resolvers.

      - *(dict) --*

        Describes a resolver.

        - **typeName** *(string) --*

          The resolver type name.

        - **fieldName** *(string) --*

          The resolver field name.

        - **dataSourceName** *(string) --*

          The resolver data source name.

        - **resolverArn** *(string) --*

          The resolver ARN.

        - **requestMappingTemplate** *(string) --*

          The request mapping template.

        - **responseMappingTemplate** *(string) --*

          The response mapping template.

        - **kind** *(string) --*

          The resolver type.

          * **UNIT** : A UNIT resolver type. A UNIT resolver is the default resolver type. A UNIT
          resolver enables you to execute a GraphQL query against a single data source.

          * **PIPELINE** : A PIPELINE resolver type. A PIPELINE resolver enables you to execute a
          series of ``Function`` in a serial manner. You can use a pipeline resolver to execute a
          GraphQL query against multiple data sources.

        - **pipelineConfig** *(dict) --*

          The ``PipelineConfig`` .

          - **functions** *(list) --*

            A list of ``Function`` objects.

            - *(string) --*

        - **syncConfig** *(dict) --*

          The ``SyncConfig`` for a resolver attached to a versioned datasource.

          - **conflictHandler** *(string) --*

            The Conflict Resolution strategy to perform in the event of a conflict.

            * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do
            not match the latest version at the server.

            * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

            * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
            LambdaConflictHandlerConfig.

          - **conflictDetection** *(string) --*

            The Conflict Detection strategy to use.

            * **VERSION** : Detect conflicts based on object versions for this resolver.

            * **NONE** : Do not detect conflicts when executing this resolver.

          - **lambdaConflictHandlerConfig** *(dict) --*

            The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

            - **lambdaConflictHandlerArn** *(string) --*

              The Arn for the Lambda function to use as the Conflict Handler.

        - **cachingConfig** *(dict) --*

          The caching configuration for the resolver.

          - **ttl** *(integer) --*

            The TTL in seconds for a resolver that has caching enabled.

            Valid values are between 1 and 3600 seconds.

          - **cachingKeys** *(list) --*

            The caching keys for a resolver that has caching enabled.

            Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

            - *(string) --*

    - **NextToken** *(string) --*

      A token to resume pagination.
    """


_ListResolversPaginatePaginationConfigTypeDef = TypedDict(
    "_ListResolversPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class ListResolversPaginatePaginationConfigTypeDef(_ListResolversPaginatePaginationConfigTypeDef):
    """
    Type definition for `ListResolversPaginate` `PaginationConfig`

    A dictionary that provides parameters to control pagination.

    - **MaxItems** *(integer) --*

      The total number of items to return. If the total number of items available is more than the
      value specified in max-items then a ``NextToken`` will be provided in the output that you can
      use to resume pagination.

    - **PageSize** *(integer) --*

      The size of each page.

    - **StartingToken** *(string) --*

      A token to specify where to start paginating. This is the ``NextToken`` from a previous
      response.
    """


_ListResolversPaginateResponseresolverscachingConfigTypeDef = TypedDict(
    "_ListResolversPaginateResponseresolverscachingConfigTypeDef",
    {"ttl": int, "cachingKeys": List[str]},
    total=False,
)


class ListResolversPaginateResponseresolverscachingConfigTypeDef(
    _ListResolversPaginateResponseresolverscachingConfigTypeDef
):
    """
    Type definition for `ListResolversPaginateResponseresolvers` `cachingConfig`

    The caching configuration for the resolver.

    - **ttl** *(integer) --*

      The TTL in seconds for a resolver that has caching enabled.

      Valid values are between 1 and 3600 seconds.

    - **cachingKeys** *(list) --*

      The caching keys for a resolver that has caching enabled.

      Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

      - *(string) --*
    """


_ListResolversPaginateResponseresolverspipelineConfigTypeDef = TypedDict(
    "_ListResolversPaginateResponseresolverspipelineConfigTypeDef",
    {"functions": List[str]},
    total=False,
)


class ListResolversPaginateResponseresolverspipelineConfigTypeDef(
    _ListResolversPaginateResponseresolverspipelineConfigTypeDef
):
    """
    Type definition for `ListResolversPaginateResponseresolvers` `pipelineConfig`

    The ``PipelineConfig`` .

    - **functions** *(list) --*

      A list of ``Function`` objects.

      - *(string) --*
    """


_ListResolversPaginateResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef = TypedDict(
    "_ListResolversPaginateResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef",
    {"lambdaConflictHandlerArn": str},
    total=False,
)


class ListResolversPaginateResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef(
    _ListResolversPaginateResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef
):
    """
    Type definition for `ListResolversPaginateResponseresolverssyncConfig`
    `lambdaConflictHandlerConfig`

    The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

    - **lambdaConflictHandlerArn** *(string) --*

      The Arn for the Lambda function to use as the Conflict Handler.
    """


_ListResolversPaginateResponseresolverssyncConfigTypeDef = TypedDict(
    "_ListResolversPaginateResponseresolverssyncConfigTypeDef",
    {
        "conflictHandler": str,
        "conflictDetection": str,
        "lambdaConflictHandlerConfig": ListResolversPaginateResponseresolverssyncConfiglambdaConflictHandlerConfigTypeDef,
    },
    total=False,
)


class ListResolversPaginateResponseresolverssyncConfigTypeDef(
    _ListResolversPaginateResponseresolverssyncConfigTypeDef
):
    """
    Type definition for `ListResolversPaginateResponseresolvers` `syncConfig`

    The ``SyncConfig`` for a resolver attached to a versioned datasource.

    - **conflictHandler** *(string) --*

      The Conflict Resolution strategy to perform in the event of a conflict.

      * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do not
      match the latest version at the server.

      * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

      * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
      LambdaConflictHandlerConfig.

    - **conflictDetection** *(string) --*

      The Conflict Detection strategy to use.

      * **VERSION** : Detect conflicts based on object versions for this resolver.

      * **NONE** : Do not detect conflicts when executing this resolver.

    - **lambdaConflictHandlerConfig** *(dict) --*

      The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

      - **lambdaConflictHandlerArn** *(string) --*

        The Arn for the Lambda function to use as the Conflict Handler.
    """


_ListResolversPaginateResponseresolversTypeDef = TypedDict(
    "_ListResolversPaginateResponseresolversTypeDef",
    {
        "typeName": str,
        "fieldName": str,
        "dataSourceName": str,
        "resolverArn": str,
        "requestMappingTemplate": str,
        "responseMappingTemplate": str,
        "kind": str,
        "pipelineConfig": ListResolversPaginateResponseresolverspipelineConfigTypeDef,
        "syncConfig": ListResolversPaginateResponseresolverssyncConfigTypeDef,
        "cachingConfig": ListResolversPaginateResponseresolverscachingConfigTypeDef,
    },
    total=False,
)


class ListResolversPaginateResponseresolversTypeDef(_ListResolversPaginateResponseresolversTypeDef):
    """
    Type definition for `ListResolversPaginateResponse` `resolvers`

    Describes a resolver.

    - **typeName** *(string) --*

      The resolver type name.

    - **fieldName** *(string) --*

      The resolver field name.

    - **dataSourceName** *(string) --*

      The resolver data source name.

    - **resolverArn** *(string) --*

      The resolver ARN.

    - **requestMappingTemplate** *(string) --*

      The request mapping template.

    - **responseMappingTemplate** *(string) --*

      The response mapping template.

    - **kind** *(string) --*

      The resolver type.

      * **UNIT** : A UNIT resolver type. A UNIT resolver is the default resolver type. A UNIT
      resolver enables you to execute a GraphQL query against a single data source.

      * **PIPELINE** : A PIPELINE resolver type. A PIPELINE resolver enables you to execute a series
      of ``Function`` in a serial manner. You can use a pipeline resolver to execute a GraphQL query
      against multiple data sources.

    - **pipelineConfig** *(dict) --*

      The ``PipelineConfig`` .

      - **functions** *(list) --*

        A list of ``Function`` objects.

        - *(string) --*

    - **syncConfig** *(dict) --*

      The ``SyncConfig`` for a resolver attached to a versioned datasource.

      - **conflictHandler** *(string) --*

        The Conflict Resolution strategy to perform in the event of a conflict.

        * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do not
        match the latest version at the server.

        * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

        * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
        LambdaConflictHandlerConfig.

      - **conflictDetection** *(string) --*

        The Conflict Detection strategy to use.

        * **VERSION** : Detect conflicts based on object versions for this resolver.

        * **NONE** : Do not detect conflicts when executing this resolver.

      - **lambdaConflictHandlerConfig** *(dict) --*

        The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

        - **lambdaConflictHandlerArn** *(string) --*

          The Arn for the Lambda function to use as the Conflict Handler.

    - **cachingConfig** *(dict) --*

      The caching configuration for the resolver.

      - **ttl** *(integer) --*

        The TTL in seconds for a resolver that has caching enabled.

        Valid values are between 1 and 3600 seconds.

      - **cachingKeys** *(list) --*

        The caching keys for a resolver that has caching enabled.

        Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

        - *(string) --*
    """


_ListResolversPaginateResponseTypeDef = TypedDict(
    "_ListResolversPaginateResponseTypeDef",
    {"resolvers": List[ListResolversPaginateResponseresolversTypeDef], "NextToken": str},
    total=False,
)


class ListResolversPaginateResponseTypeDef(_ListResolversPaginateResponseTypeDef):
    """
    Type definition for `ListResolversPaginate` `Response`

    - **resolvers** *(list) --*

      The ``Resolver`` objects.

      - *(dict) --*

        Describes a resolver.

        - **typeName** *(string) --*

          The resolver type name.

        - **fieldName** *(string) --*

          The resolver field name.

        - **dataSourceName** *(string) --*

          The resolver data source name.

        - **resolverArn** *(string) --*

          The resolver ARN.

        - **requestMappingTemplate** *(string) --*

          The request mapping template.

        - **responseMappingTemplate** *(string) --*

          The response mapping template.

        - **kind** *(string) --*

          The resolver type.

          * **UNIT** : A UNIT resolver type. A UNIT resolver is the default resolver type. A UNIT
          resolver enables you to execute a GraphQL query against a single data source.

          * **PIPELINE** : A PIPELINE resolver type. A PIPELINE resolver enables you to execute a
          series of ``Function`` in a serial manner. You can use a pipeline resolver to execute a
          GraphQL query against multiple data sources.

        - **pipelineConfig** *(dict) --*

          The ``PipelineConfig`` .

          - **functions** *(list) --*

            A list of ``Function`` objects.

            - *(string) --*

        - **syncConfig** *(dict) --*

          The ``SyncConfig`` for a resolver attached to a versioned datasource.

          - **conflictHandler** *(string) --*

            The Conflict Resolution strategy to perform in the event of a conflict.

            * **OPTIMISTIC_CONCURRENCY** : Resolve conflicts by rejecting mutations when versions do
            not match the latest version at the server.

            * **AUTOMERGE** : Resolve conflicts with the Automerge conflict resolution strategy.

            * **LAMBDA** : Resolve conflicts with a Lambda function supplied in the
            LambdaConflictHandlerConfig.

          - **conflictDetection** *(string) --*

            The Conflict Detection strategy to use.

            * **VERSION** : Detect conflicts based on object versions for this resolver.

            * **NONE** : Do not detect conflicts when executing this resolver.

          - **lambdaConflictHandlerConfig** *(dict) --*

            The ``LambdaConflictHandlerConfig`` when configuring LAMBDA as the Conflict Handler.

            - **lambdaConflictHandlerArn** *(string) --*

              The Arn for the Lambda function to use as the Conflict Handler.

        - **cachingConfig** *(dict) --*

          The caching configuration for the resolver.

          - **ttl** *(integer) --*

            The TTL in seconds for a resolver that has caching enabled.

            Valid values are between 1 and 3600 seconds.

          - **cachingKeys** *(list) --*

            The caching keys for a resolver that has caching enabled.

            Valid values are entries from the ``$context.identity`` and ``$context.arguments`` maps.

            - *(string) --*

    - **NextToken** *(string) --*

      A token to resume pagination.
    """


_ListTypesPaginatePaginationConfigTypeDef = TypedDict(
    "_ListTypesPaginatePaginationConfigTypeDef",
    {"MaxItems": int, "PageSize": int, "StartingToken": str},
    total=False,
)


class ListTypesPaginatePaginationConfigTypeDef(_ListTypesPaginatePaginationConfigTypeDef):
    """
    Type definition for `ListTypesPaginate` `PaginationConfig`

    A dictionary that provides parameters to control pagination.

    - **MaxItems** *(integer) --*

      The total number of items to return. If the total number of items available is more than the
      value specified in max-items then a ``NextToken`` will be provided in the output that you can
      use to resume pagination.

    - **PageSize** *(integer) --*

      The size of each page.

    - **StartingToken** *(string) --*

      A token to specify where to start paginating. This is the ``NextToken`` from a previous
      response.
    """


_ListTypesPaginateResponsetypesTypeDef = TypedDict(
    "_ListTypesPaginateResponsetypesTypeDef",
    {"name": str, "description": str, "arn": str, "definition": str, "format": str},
    total=False,
)


class ListTypesPaginateResponsetypesTypeDef(_ListTypesPaginateResponsetypesTypeDef):
    """
    Type definition for `ListTypesPaginateResponse` `types`

    Describes a type.

    - **name** *(string) --*

      The type name.

    - **description** *(string) --*

      The type description.

    - **arn** *(string) --*

      The type ARN.

    - **definition** *(string) --*

      The type definition.

    - **format** *(string) --*

      The type format: SDL or JSON.
    """


_ListTypesPaginateResponseTypeDef = TypedDict(
    "_ListTypesPaginateResponseTypeDef",
    {"types": List[ListTypesPaginateResponsetypesTypeDef], "NextToken": str},
    total=False,
)


class ListTypesPaginateResponseTypeDef(_ListTypesPaginateResponseTypeDef):
    """
    Type definition for `ListTypesPaginate` `Response`

    - **types** *(list) --*

      The ``Type`` objects.

      - *(dict) --*

        Describes a type.

        - **name** *(string) --*

          The type name.

        - **description** *(string) --*

          The type description.

        - **arn** *(string) --*

          The type ARN.

        - **definition** *(string) --*

          The type definition.

        - **format** *(string) --*

          The type format: SDL or JSON.

    - **NextToken** *(string) --*

      A token to resume pagination.
    """
