-- Sentinel Control Tower — Supabase (Postgres) schema
-- Run this in the Supabase SQL editor, then use backend/data/generate_data.py
-- output CSVs (or scripts/seed_supabase.py) to load seed data.

create table if not exists suppliers (
    supplier_id text primary key,
    name text not null,
    tier smallint not null check (tier in (1,2,3)),
    location text not null,
    lead_time_days integer not null,
    unit_cost numeric not null,
    capacity_units integer not null,
    reliability_score numeric not null,
    backup_for text references suppliers(supplier_id)
);

create table if not exists products (
    product_id text primary key,
    name text not null,
    category text not null,
    unit_price numeric not null,
    unit_cost numeric not null,
    safety_stock integer not null,
    reorder_point integer not null,
    lead_time_days integer not null,
    supplier_id text references suppliers(supplier_id)
);

create table if not exists warehouses (
    warehouse_id text primary key,
    name text not null,
    location text not null,
    capacity_units integer not null,
    holding_cost_per_unit_day numeric not null
);

create table if not exists inventory (
    inventory_id text primary key,
    product_id text references products(product_id),
    warehouse_id text references warehouses(warehouse_id),
    quantity_on_hand integer not null,
    quantity_in_transit integer not null default 0,
    last_updated timestamptz not null default now()
);

create table if not exists orders (
    order_id text primary key,
    product_id text references products(product_id),
    warehouse_id text references warehouses(warehouse_id),
    customer_id text not null,
    customer_tier text not null check (customer_tier in ('A','B','C')),
    quantity integer not null,
    order_date date not null,
    promised_delivery_date date not null,
    priority_score numeric not null,
    status text not null check (status in ('pending','in_transit','delivered','delayed','cancelled'))
);

create table if not exists disruption_events (
    event_id text primary key,
    event_type text not null,
    affected_supplier_id text references suppliers(supplier_id),
    affected_region text not null,
    detected_date date not null,
    severity numeric not null check (severity >= 0 and severity <= 1),
    predicted_delay_days integer not null,
    source text not null,
    description text
);

create table if not exists demand_history (
    id bigserial primary key,
    product_id text references products(product_id),
    date date not null,
    quantity integer not null
);

create table if not exists action_plans (
    id bigserial primary key,
    event_id text references disruption_events(event_id),
    lever smallint not null check (lever between 1 and 5),
    description text,
    estimated_cost numeric,
    expected_stockout_reduction numeric,
    sla_impact numeric,
    rank smallint
);

create table if not exists recommendations (
    id bigserial primary key,
    event_id text references disruption_events(event_id),
    best_action_plan_id bigint references action_plans(id),
    explanation_text text,
    created_at timestamptz not null default now()
);

create table if not exists audit_log (
    id bigserial primary key,
    user_action text not null,
    entity text not null,
    entity_id text,
    timestamp timestamptz not null default now(),
    payload jsonb
);

-- Helpful indexes
create index if not exists idx_products_supplier on products(supplier_id);
create index if not exists idx_inventory_product on inventory(product_id);
create index if not exists idx_inventory_warehouse on inventory(warehouse_id);
create index if not exists idx_orders_product on orders(product_id);
create index if not exists idx_orders_status on orders(status);
create index if not exists idx_events_supplier on disruption_events(affected_supplier_id);
create index if not exists idx_demand_product_date on demand_history(product_id, date);
