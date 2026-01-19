"""
SINGLE ENDPOINT CRUD API - ONE ROUTE TO RULE THEM ALL

WARNING: This API puts all CRUD operations through one POST endpoint.

What this does:
All Create, Read, Update, Delete operations go through POST /api
The operation type is specified via "action" field in the request body.

The correct way:
    POST   /api/items         {"name": "..."}       # Create
    GET    /api/items/{id}                          # Read
    PUT    /api/items/{id}    {"name": "..."}       # Update
    DELETE /api/items/{id}                          # Delete
    GET    /api/items                               # List all

The cursed way:
    POST /api {"action": "create", "id": "1", "name": "..."}
    POST /api {"action": "list"}
    POST /api {"action": "update", "id": "1", "name": "..."}
    POST /api {"action": "delete", "id": "1"}

Everything through one endpoint. HTTP methods are just suggestions.

Why this violates REST principles:

1. IGNORES HTTP METHOD SEMANTICS:
   HTTP methods have meaning:
   - GET: Safe, idempotent, cacheable
   - POST: Creates resources, not idempotent
   - PUT: Updates resources, idempotent
   - DELETE: Removes resources, idempotent

   This API: POST for everything, semantics in body

2. NOT RESTFUL RESOURCE DESIGN:
   REST uses resource URLs:
   - /items (collection)
   - /items/123 (specific resource)

   This API: /api for everything, resource in body

3. BREAKS HTTP CACHING:
   GET requests are cached by browsers/proxies
   POST requests are not cached

   Result: "list" action can't be cached even though it's a read operation

4. NO IDEMPOTENCY WHERE EXPECTED:
   PUT and DELETE should be idempotent (same result if called multiple times)
   This uses POST for everything, which is not idempotent by spec

5. POOR DISCOVERABILITY:
   RESTful API: Look at URLs and methods to understand what's available
   This API: Need to read docs to know valid "action" strings

6. RETURNS ENTIRE STATE:
   Every operation returns the full items dict

   Problems:
   - Leaks all data to anyone who makes a request
   - Bandwidth waste (returning everything for single item operations)
   - Privacy/security issue
   - Scales poorly (imagine returning 1M items after creating one)

7. ID IN BODY FOR ALL OPERATIONS:
   REST: Resource ID in URL (/items/123)
   This: Resource ID in request body

   Issues:
   - Can't bookmark specific resources
   - Can't share URLs to resources
   - URL doesn't identify the resource

8. NO HTTP STATUS SEMANTICS:
   REST conventions:
   - 201 Created: Resource successfully created
   - 200 OK: Successful read/update
   - 204 No Content: Successful delete (no body needed)
   - 404 Not Found: Resource doesn't exist
   - 409 Conflict: Resource already exists

   This API: Everything returns 200 (except errors return 400/404)
   Missing: 201 for creation, 204 for deletion

9. SINGLE POINT OF FAILURE:
   One route handles everything
   If /api breaks, entire API is down

   RESTful: Multiple routes, partial degradation possible

10. VIOLATES PRINCIPLE OF LEAST SURPRISE:
    Every developer expects CRUD to map to HTTP methods
    This API surprises everyone with "action" field

Real-world consequences:

Issue 1 - API Gateway Rate Limiting:
    Gateway: "Limit POST to 10/minute, GET to 100/minute"
    This API: "Everything is POST"
    Result: Read operations get severely rate limited

Issue 2 - Monitoring and Logging:
    Monitor: "Show all failed GET requests"
    This API: "They're all POST"
    Result: Can't distinguish read vs write failures in logs

Issue 3 - Browser Behavior:
    Browser: "User clicked back button, show cached GET response"
    This API: "My reads are POST, no caching"
    Result: Extra server requests, slower UX

Issue 4 - Load Balancer:
    Balancer: "POST /api gets 100 requests/second"
    Balancer: "Can't tell if they're reads (fast) or writes (slow)"
    Result: Poor routing decisions

Issue 5 - Data Leak:
    User: Creates one item
    Response: {"message": "created", "items": {...entire database...}}
    User: "Why can I see everyone else's data?"

Performance comparison:

RESTful approach:
    POST /api/items {"name": "item1"}
    Response: {"id": "1", "name": "item1"}
    Size: ~30 bytes

This approach:
    POST /api {"action": "create", "id": "1", "name": "item1"}
    Response: {"message": "created", "items": {entire database}}
    Size: 30 bytes + entire database size

With 1000 items: Response is 100x larger than needed

The correct RESTful design:

@app.route("/api/items", methods=["POST"])
def create_item():
    data = request.get_json()
    item_id = str(len(items) + 1)
    items[item_id] = data.get("name")
    return jsonify({"id": item_id, "name": items[item_id]}), 201

@app.route("/api/items/<item_id>", methods=["GET"])
def get_item(item_id):
    if item_id not in items:
        return jsonify({"error": "not found"}), 404
    return jsonify({"id": item_id, "name": items[item_id]})

@app.route("/api/items/<item_id>", methods=["PUT"])
def update_item(item_id):
    if item_id not in items:
        return jsonify({"error": "not found"}), 404
    data = request.get_json()
    items[item_id] = data.get("name")
    return jsonify({"id": item_id, "name": items[item_id]})

@app.route("/api/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    if item_id not in items:
        return jsonify({"error": "not found"}), 404
    del items[item_id]
    return '', 204

@app.route("/api/items", methods=["GET"])
def list_items():
    return jsonify({"items": items})

Clear routes, semantic methods, proper status codes, resource-oriented.

Additional problems with this implementation:

1. NO AUTHENTICATION:
   Anyone can create, update, delete anything
   No API keys, no tokens, nothing

2. NO INPUT VALIDATION:
   What if name is 10 GB?
   What if id contains SQL/code?
   Minimal validation

3. NO RATE LIMITING:
   Single endpoint easily DDoS'd
   No throttling, no protection

4. DEBUG MODE:
   app.run(debug=True) in production:
   - Exposes stack traces
   - Allows code execution via debugger
   - Security nightmare

5. IN-MEMORY STORAGE:
   items = {}
   Lost on restart, no persistence

6. NO VERSIONING:
   API changes break all clients
   No /v1/, /v2/ versioning

7. NO PAGINATION:
   "list" action returns everything
   Imagine 1 million items

8. GLOBAL MUTABLE STATE:
   All users share one dict
   No isolation, no multi-tenancy

9. NOT THREAD-SAFE:
   Concurrent modifications to items dict
   Race conditions possible

Historical context:
This pattern is similar to:
- SOAP (everything over POST, operation in body)
- RPC-style APIs (procedure calls, not resources)
- Pre-REST API designs from 2000s

We learned these patterns have issues, which is why REST emerged.

Educational value:
- Shows why HTTP methods exist
- Demonstrates REST principles by violating them
- Illustrates resource-oriented vs action-oriented design
- Proves conventions exist for good reasons

Real-world analogy:
This is like a restaurant with one phone number and one person
who handles all orders. Instead of calling:
- Reservations line
- Takeout line
- Catering line

You call one number and say:
"Hi, action is 'reserve', details are..."

It works, but it's inefficient and confusing.

When is this pattern acceptable?
- GraphQL (designed for single endpoint, has type system)
- JSON-RPC (explicit RPC protocol)
- Internal microservices (sometimes)
- Never for public REST APIs

Author's note: Flask supports multiple routes and methods natively.
                I chose to cram everything into one POST endpoint.
                Roy Fielding is having an aneurysm.
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory demo data (lost on restart, no persistence)
items = {}


def handle_create(data):
    """
    Create handler - should be POST /api/items
    Instead: POST /api with action="create"

    Returns entire items dict after creation (data leak)
    """
    item_id = data.get("id")
    name = data.get("name")

    if not item_id or not name:
        return {"error": "id and name required"}, 400

    # No check if item already exists (should return 409 Conflict)
    items[item_id] = name

    # Returns entire database state (scales poorly)
    return {"message": "created", "items": items}, 200


def handle_update(data):
    """
    Update handler - should be PUT /api/items/{id}
    Instead: POST /api with action="update"

    Returns entire items dict after update (unnecessary)
    """
    item_id = data.get("id")
    name = data.get("name")

    if item_id not in items:
        return {"error": "item not found"}, 404

    items[item_id] = name

    # Again, returns entire database
    return {"message": "updated", "items": items}, 200


def handle_delete(data):
    """
    Delete handler - should be DELETE /api/items/{id}
    Instead: POST /api with action="delete"

    Returns entire remaining items (why?)
    """
    item_id = data.get("id")

    if item_id not in items:
        return {"error": "item not found"}, 404

    del items[item_id]

    # Returning all remaining items after deletion.... crazy right?
    return {"message": "deleted", "items": items}, 200


def handle_list(data):
    """
    List handler - should be GET /api/items
    Instead: POST /api with action="list"

    At least this one returning everything makes sense.
    But it's a POST request for a read operation (not cacheable).
    """
    # data parameter unused but kept for consistent handler signature, yes... I told it to shut up.
    _ = data
    return {"items": items}, 200


# Single POST endpoint (ignoring HTTP method semantics)
@app.route("/api", methods=["POST"])
def api_router():
    """
    The one endpoint to rule them all.

    Handles create, update, delete, and list via "action" field.
    Completely ignores HTTP methods (GET, POST, PUT, DELETE).

    Every request is POST, operation specified in body.
    This is not RESTful. This is RPC pretending to be REST.

    curl examples:

    Create:
        curl -X POST http://localhost:5000/api \
             -H "Content-Type: application/json" \
             -d '{"action":"create","id":"1","name":"item1"}'

    List:
        curl -X POST http://localhost:5000/api \
             -H "Content-Type: application/json" \
             -d '{"action":"list"}'

    Update:
        curl -X POST http://localhost:5000/api \
             -H "Content-Type: application/json" \
             -d '{"action":"update","id":"1","name":"updated"}'

    Delete:
        curl -X POST http://localhost:5000/api \
             -H "Content-Type: application/json" \
             -d '{"action":"delete","id":"1"}'

    Notice: Every curl uses -X POST. The operation is in the data.
    This is what we're trying to avoid with REST.
    """
    body = request.get_json()

    if not body:
        return jsonify({"error": "invalid json"}), 400

    # String comparison dispatch (poor man's routing)
    action = body.get("action")

    if action == "create":
        response, status = handle_create(body)
    elif action == "update":
        response, status = handle_update(body)
    elif action == "delete":
        response, status = handle_delete(body)
    elif action == "list":
        response, status = handle_list(body)
    else:
        response, status = {"error": "unknown action"}, 400

    return jsonify(response), status

#why am I here? Just to suffer?......


if __name__ == "__main__":
    # debug=True exposes stack traces and debug console
    # Never use in production
    app.run(debug=True)