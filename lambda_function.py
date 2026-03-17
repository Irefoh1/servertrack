import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ServerInventory')


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)


def build_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        },
        'body': json.dumps(body, cls=DecimalEncoder)
    }


def get_all_servers():
    response = table.scan()
    return build_response(200, {
        'servers': response.get('Items', []),
        'count': response.get('Count', 0)
    })


def get_server(server_id):
    response = table.get_item(Key={'server_id': server_id})
    if 'Item' in response:
        return build_response(200, response['Item'])
    return build_response(404, {'message': 'Server not found'})


def create_server(body):
    required = ['server_name', 'environment', 'instance_type', 'ip_address', 'region', 'team']
    for field in required:
        if field not in body:
            return build_response(400, {'message': f'Missing required field: {field}'})

    item = {
        'server_id': str(uuid.uuid4()),
        'server_name': body['server_name'],
        'environment': body['environment'],
        'instance_type': body['instance_type'],
        'ip_address': body['ip_address'],
        'region': body['region'],
        'team': body['team'],
        'status': body.get('status', 'running'),
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }

    table.put_item(Item=item)
    return build_response(201, {'message': 'Server created', 'server': item})


def update_server(server_id, body):
    response = table.get_item(Key={'server_id': server_id})
    if 'Item' not in response:
        return build_response(404, {'message': 'Server not found'})

    update_expr_parts = []
    expr_values = {}
    expr_names = {}

    allowed_fields = ['server_name', 'environment', 'instance_type',
                      'ip_address', 'region', 'team', 'status']

    for field in allowed_fields:
        if field in body:
            update_expr_parts.append(f'#{field} = :{field}')
            expr_values[f':{field}'] = body[field]
            expr_names[f'#{field}'] = field

    update_expr_parts.append('#updated_at = :updated_at')
    expr_values[':updated_at'] = datetime.utcnow().isoformat()
    expr_names['#updated_at'] = 'updated_at'

    table.update_item(
        Key={'server_id': server_id},
        UpdateExpression='SET ' + ', '.join(update_expr_parts),
        ExpressionAttributeValues=expr_values,
        ExpressionAttributeNames=expr_names
    )

    return build_response(200, {'message': 'Server updated'})


def delete_server(server_id):
    response = table.get_item(Key={'server_id': server_id})
    if 'Item' not in response:
        return build_response(404, {'message': 'Server not found'})

    table.delete_item(Key={'server_id': server_id})
    return build_response(200, {'message': 'Server deleted'})


def lambda_handler(event, context):
    http_method = event.get('httpMethod', '')
    path = event.get('path', '')
    path_params = event.get('pathParameters') or {}

    if http_method == 'OPTIONS':
        return build_response(200, {'message': 'OK'})

    try:
        if path == '/servers' and http_method == 'GET':
            return get_all_servers()

        elif path == '/servers' and http_method == 'POST':
            body = json.loads(event.get('body', '{}'))
            return create_server(body)

        elif '/servers/' in path and http_method == 'GET':
            return get_server(path_params['server_id'])

        elif '/servers/' in path and http_method == 'PUT':
            body = json.loads(event.get('body', '{}'))
            return update_server(path_params['server_id'], body)

        elif '/servers/' in path and http_method == 'DELETE':
            return delete_server(path_params['server_id'])

        else:
            return build_response(404, {'message': 'Route not found'})

    except Exception as e:
        print(f'Error: {str(e)}')
        return build_response(500, {'message': 'Internal server error'})