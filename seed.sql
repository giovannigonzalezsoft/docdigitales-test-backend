-- ---------------------------------------------------------
-- Clients
-- ---------------------------------------------------------

INSERT INTO clients (
    id,
    name,
    rfc
)
VALUES
    (
        1,
        'Comercializadora del Norte SA de CV',
        'CNO010101AB1'
    ),
    (
        2,
        'Servicios Empresariales MX SA de CV',
        'SEM020202CD2'
    );


-- ---------------------------------------------------------
-- Invoices
-- ---------------------------------------------------------

INSERT INTO invoices (
    id,
    client_id,
    folio,
    total,
    status,
    issue_date
)
VALUES
    (
        1,
        1,
        'FAC-001',
        1500.50,
        'pendiente',
        '2026-09-20'
    ),
    (
        2,
        1,
        'FAC-002',
        2500.00,
        'vencida',
        '2026-09-21'
    ),
    (
        3,
        2,
        'FAC-003',
        850.75,
        'pendiente',
        '2026-09-22'
    ),
    (
        4,
        2,
        'FAC-004',
        1200.00,
        'vencida',
        '2026-09-23'
    );


-- ---------------------------------------------------------
-- Payments
-- ---------------------------------------------------------

INSERT INTO payments (
    id,
    invoice_id,
    amount,
    payment_date
)
VALUES
    (
        1,
        1,
        500.00,
        '2026-09-24'
    ),
    (
        2,
        1,
        250.00,
        '2026-09-25'
    ),
    (
        3,
        2,
        1000.00,
        '2026-09-26'
    );


-- ---------------------------------------------------------
-- Reset sequences
-- ---------------------------------------------------------

SELECT setval(
    pg_get_serial_sequence('clients', 'id'),
    (SELECT MAX(id) FROM clients)
);

SELECT setval(
    pg_get_serial_sequence('invoices', 'id'),
    (SELECT MAX(id) FROM invoices)
);

SELECT setval(
    pg_get_serial_sequence('payments', 'id'),
    (SELECT MAX(id) FROM payments)
);