AUTH
────────────────────────
POST   /auth/register
POST   /auth/login


USERS
────────────────────────
GET    /users/me
PUT    /users/me
DELETE /users/me


BANKS
────────────────────────
POST   /banks
GET    /banks
DELETE /banks/{account_id}


SECURITIES
────────────────────────
GET    /securities
GET    /securities/{security_id}


HOLDINGS
────────────────────────
GET    /holdings
GET    /holdings/{holding_id}


ORDERS
────────────────────────
POST   /orders
GET    /orders
GET    /orders/{order_id}
DELETE /orders/{order_id}


EXECUTIONS
────────────────────────
GET    /executions
GET    /executions/{execution_id}