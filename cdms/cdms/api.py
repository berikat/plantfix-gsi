import frappe
from frappe.utils.response import build_response
from frappe import _

@frappe.whitelist()
def get_item(from_date=None, to_date=None, limit_start=None, limit_page_length=None):
    if not limit_page_length:
        limit_page_length = 20
    if not limit_start:
        limit_start = 0 
    datalist = frappe.db.sql("""SELECT `item_code`, `item_name`, `item_group`, `weight_per_unit`
, `country_of_origin`, `stock_uom`, `is_fixed_asset` 
FROM tabItem a WHERE `docstatus` != 2 and a.modified >= %s and a.modified < %s
order by a.`name`
limit %s,%s""", (from_date, to_date, int(limit_start), int(limit_page_length)), as_dict=True)
    return get_response(datalist)

@frappe.whitelist()
def get_uom(from_date=None, to_date=None, limit_start=None, limit_page_length=None):
    if not limit_page_length:
        limit_page_length = 20
    if not limit_start:
        limit_start = 0 
    datalist = frappe.db.sql("""SELECT a.`name` 
FROM `tabUOM` a WHERE `docstatus` != 2 and a.modified >= %s and a.modified < %s
order by a.`name`
limit %s,%s""", (from_date, to_date, int(limit_start), int(limit_page_length)), as_dict=True)
    return get_response(datalist)

@frappe.whitelist()
def get_customer_supplier(from_date=None, to_date=None, limit_start=None, limit_page_length=None):
    if not limit_page_length:
        limit_page_length = 20
    if not limit_start:
        limit_start = 0 
    datalist = frappe.db.sql("""select * from (SELECT c.`customer_name` as `name`
, c.`facility_type`
, c.`tax_id`
, c.`facility_number`
, c.`facility_date`
, c.`name` as `code`
, c.`default_currency`
, c.modified
, (
	SELECT country
	FROM `tabAddress` addr 
	join `tabDynamic Link` l ON l.`link_doctype` = 'Customer' 
									AND l.parenttype = 'Address'
									AND l.parent = addr.`name`
	WHERE l.link_name = c.`name`
	LIMIT 1
  ) AS country
FROM tabCustomer c
UNION
SELECT s.`supplier_name` as `name` 
, s.`facility_type`
, s.`tax_id`
, s.`facility_number`
, s.`facility_date`
, s.`name` as `code`
, s.`default_currency`
, s.modified
, (
	SELECT country
	FROM `tabAddress` addr 
	join `tabDynamic Link` l ON l.`link_doctype` = 'Supplier' 
									AND l.parenttype = 'Address'
									AND l.parent = addr.`name`
	WHERE l.link_name = s.`name`
	LIMIT 1
  ) AS country
FROM tabSupplier s) as cs 
where cs.modified >= %s and cs.modified < %s
order by cs.`name`
limit %s,%s""", (from_date, to_date, int(limit_start), int(limit_page_length)), as_dict=True)
    return get_response(datalist)

@frappe.whitelist()
def get_customer_supplier_address(from_date=None, to_date=None, limit_start=None, limit_page_length=None):
    if not limit_page_length:
        limit_page_length = 20
    if not limit_start:
        limit_start = 0 
    datalist = frappe.db.sql("""select * from (SELECT a.`name`
, c.address_title
, c.address_line1
, c.address_line2
, c.is_primary_address
, c.pincode
, c.city
, c.state
, case when c.modified > a.modified then c.modified else a.modified end modified
FROM `tabCustomer` a
JOIN `tabDynamic Link` b ON b.link_doctype = 'Customer' AND b.link_name = a.`name` AND b.parenttype = 'Address'
JOIN `tabAddress` c ON c.`name` = b.parent
UNION
SELECT a.`name`
, c.address_title
, c.address_line1
, c.address_line2
, c.is_primary_address
, c.pincode
, c.city
, c.state
, case when c.modified > a.modified then c.modified else a.modified end modified
FROM `tabSupplier` a
JOIN `tabDynamic Link` b ON b.link_doctype = 'Supplier' AND b.link_name = a.`name` AND b.parenttype = 'Address'
JOIN `tabAddress` c ON c.`name` = b.parent) as cs 
where cs.modified >= %s and cs.modified < %s
order by cs.`name`, cs.address_title
limit %s,%s""", (from_date, to_date, int(limit_start), int(limit_page_length)), as_dict=True)
    return get_response(datalist)

@frappe.whitelist()
def get_receiving(from_date=None, to_date=None, limit_start=None, limit_page_length=None):
    if not limit_page_length:
        limit_page_length = 20
    if not limit_start:
        limit_start = 0 
    datalist = frappe.db.sql("""select * from (SELECT pr.company AS `Company`
, pr.`name` AS `ExternalId`
, sup.`name` AS `SupplierCode`
, sup.`supplier_name` AS `SupplierName`
, pr.posting_date AS `ReceiptDate`
, pr.`name` AS `ReceiptNumber`
, pri.item_code AS `Code`
, pri.item_name AS `Description`
, pri.stock_qty AS `Quantity`
, pri.stock_uom AS `Uom`
, pri.received_qty AS `QuantityInput`
, pri.uom AS `UomInput`
, pr.currency AS `Currency`
, pri.rate AS `UnitPrice`
, pri.amount AS `Amount`
, pri.base_amount AS `BaseAmount`
, pr.`bc_type` AS `BcType`
, pr.`bc_number` AS `BcNumber`
, pr.`bc_date` AS `BcDate`
, pr.`total` AS `TotalAmount`
, pr.`base_total` AS `TotalBaseAmount`
, pr.`total_taxes_and_charges` AS `TotalTaxAmount`
, pr.`base_total_taxes_and_charges` AS `TotalBaseTaxAmount`
, inv.`bill_no` AS `InvoiceNo`
, inv.`bill_date` AS `InvoiceDate`
, case when pri.modified > pr.modified then pri.modified else pr.modified end modified
FROM `tabPurchase Receipt` pr
JOIN `tabPurchase Receipt Item` pri ON pr.`name` = pri.`parent` and pri.parenttype = 'Purchase Receipt'
JOIN `tabSupplier` sup ON pr.`supplier` = sup.`name`
LEFT JOIN `tabPurchase Invoice Item` invi ON pr.`name` = invi.`purchase_receipt` AND invi.`parenttype` = 'Purchase Invoice'
LEFT JOIN `tabPurchase Invoice` inv ON invi.`parent` = inv.`name`
WHERE pr.docstatus = 1
UNION	
SELECT se.company AS `Company`
, se.`name` AS `ExternalId`
, sup.`name` AS `SupplierCode`
, sup.`supplier_name` AS `SupplierName`
, se.posting_date AS `ReceiptDate`
, se.`name` AS `ReceiptNumber`
, sei.item_code AS `Code`
, sei.description AS `Description`
, sei.transfer_qty AS `Quantity`
, sei.stock_uom AS `Uom`
, sei.qty AS `QuantityInput`
, sei.uom AS `UomInput`
, comp.default_currency AS `Currency`
, sei.valuation_rate AS `UnitPrice`
, sei.amount AS `Amount`
, sei.amount AS `BaseAmount`
, se.`bc_type` AS `BcType`
, se.`bc_number` AS `BcNumber`
, se.`bc_date` AS `BcDate`
, se.`total_amount` AS `TotalAmount`
, se.`total_amount` AS `TotalBaseAmount`
, 0 AS `TotalTaxAmount`
, 0 AS `TotalBaseTaxAmount`
, NULL AS `InvoiceNo`
, NULL AS `InvoiceDate` 
, case when sei.modified > se.modified then sei.modified else se.modified end modified
FROM `tabStock Entry` se
JOIN `tabStock Entry Detail` sei ON se.`name` = sei.`parent` and sei.parenttype = 'Stock Entry'
JOIN `tabCompany` comp ON se.company = comp.`name`
LEFT JOIN `tabSupplier` sup ON se.`supplier_bc` = sup.`name`
WHERE se.docstatus = 1 AND se.purpose = 'Material Receipt') as cs 
where cs.modified >= %s and cs.modified < %s
order by cs.`ExternalId`
limit %s,%s""", (from_date, to_date, int(limit_start), int(limit_page_length)), as_dict=True)
    return get_response(datalist)

@frappe.whitelist()
def get_outgoing(from_date=None, to_date=None, limit_start=None, limit_page_length=None):
    if not limit_page_length:
        limit_page_length = 20
    if not limit_start:
        limit_start = 0 
    datalist = frappe.db.sql("""select dn.company AS `Company`
, dn.`name` AS `ExternalId`
, dn.`customer` AS `CustomerCode`
, dn.`customer_name` AS `CustomerName`
, dn.posting_date AS `OutgoingDate`
, dn.`name` AS `OutgoingNumber`
, dni.item_code AS `Code`
, dni.item_name AS `Description`
, dni.stock_qty AS `Quantity`
, dni.stock_uom AS `Uom`
, dni.uom AS `UomInput`
, dn.currency AS `Currency`
, dni.rate AS `UnitPrice`
, dn.base_grand_total AS `Amount`
, dn.`type_of_customs_document` AS `BcType`
, dn.`number_of_customs_document` AS `BcNumber`
, dn.`date_of_customs_document` AS `BcDate`
, inv.`name` AS `InvoiceNo`
, inv.`posting_date` AS `InvoiceDate`
, case when dni.modified > dn.modified then dni.modified else dn.modified end modified
FROM `tabDelivery Note` dn
JOIN `tabDelivery Note Item` dni ON dn.`name` = dni.`parent` and dni.`parenttype` = 'Delivery Note'
JOIN `tabCustomer` cus ON dn.`customer` = cus.`name`
LEFT JOIN `tabSales Invoice Item` invi ON dn.`name` = invi.`delivery_note` AND invi.`parenttype` = 'Sales Invoice'
LEFT JOIN `tabSales Invoice` inv ON invi.`parent` = inv.`name`
where dn.modified >= %s and dn.modified < %s
    order by dn.`ExternalId`
limit %s,%s""", (from_date, to_date, int(limit_start), int(limit_page_length)), as_dict=True)
    return get_response(datalist)

@frappe.whitelist()
def get_bom(from_date=None, to_date=None, limit_start=None, limit_page_length=None):
    if not limit_page_length:
        limit_page_length = 20
    if not limit_start:
        limit_start = 0 
    datalist = frappe.db.sql("""select a.name as BomCode
	, a.is_default as IsDefault
    , a.is_active as IsActive
    , a.item as ProductCode
    , b.item_code as MaterialCode
    , b.bom_no as MaterialBomCode
    , b.stock_qty as Quantity
    , b.stock_uom as UomName
    , a.remark Remark
from `tabBOM` a
inner join `tabBOM Item` b on a.name = b.parent
where a.docstatus = 1 and a.modified >= %s and a.modified < %s
order by a.`name`
limit %s,%s""", (from_date, to_date, int(limit_start), int(limit_page_length)), as_dict=True)
    return get_response(datalist)

@frappe.whitelist()
def get_bom_scrap(from_date=None, to_date=None, limit_start=None, limit_page_length=None):
    if not limit_page_length:
        limit_page_length = 20
    if not limit_start:
        limit_start = 0 
    datalist = frappe.db.sql("""select a.name as BomCode
	, a.item as ProductCode
    , b.item_code as MaterialCode
    , b.stock_qty / a.quantity as Quantity
    , b.stock_uom as UomCode
from `tabBOM` a
inner join `tabBOM Scrap Item` b on a.name = b.parent
where a.docstatus = 1 and a.modified >= %s and a.modified < %s
order by a.`name`
limit %s,%s""", (from_date, to_date, int(limit_start), int(limit_page_length)), as_dict=True)
    return get_response(datalist)

@frappe.whitelist()
def get_movement_stock(from_date=None, to_date=None, limit_start=None, limit_page_length=None):
    if not limit_page_length:
        limit_page_length = 20
    if not limit_start:
        limit_start = 0 
    datalist = frappe.db.sql("""SELECT 
a.`name` transaction_id
, a.company
, a.voucher_no transaction_number
, a.posting_date
, case when a.voucher_type = 'Stock Entry' then b.title ELSE a.voucher_type end transaction_type
, case when a.voucher_type = 'Stock Entry' then a.warehouse END from_warehouse
, coalesce(b.to_warehouse, a.warehouse) to_warehouse
, a.item_code
, a.stock_uom uom_code
, case when a.actual_qty = 0 then a.qty_after_transaction else a.actual_qty end quantity
, (case when a.actual_qty = 0 then a.qty_after_transaction else a.actual_qty end) * a.valuation_rate cost
, a.creation
, a.modified
FROM `tabStock Ledger Entry` a
LEFT JOIN `tabStock Entry` b ON a.voucher_no = b.`name` AND a.voucher_type = 'Stock Entry'
WHERE a.docstatus != 2 and a.modified >= %s and a.modified < %s
order by a.`name`
limit %s,%s""", (from_date, to_date, int(limit_start), int(limit_page_length)), as_dict=True)
    return get_response(datalist)

@frappe.whitelist()
def get_invoice(from_date=None, to_date=None, limit_start=None, limit_page_length=None):
    if not limit_page_length:
        limit_page_length = 20
    if not limit_start:
        limit_start = 0 
    datalist = frappe.db.sql("""SELECT 
concat(a.`name`,'-',b.`name`) id
, a.`name` invoice_number
, a.company
, a.posting_date invoice_date
, a.title account_name
, c.`name` account_code
, b.item_code
, b.item_name
, b.qty
, b.uom
, b.rate unit_price
, b.amount
, a.currency
, b.total_weight net_weight
, a.modified
, a.remark_sales_invoice
, a.docstatus
, b.bom
FROM `tabSales Invoice` a
JOIN `tabSales Invoice Item` b ON a.`name` = b.`parent` AND b.`parenttype` = 'Sales Invoice'
JOIN `tabCustomer` c ON a.title = c.`name`
WHERE a.modified >= %s and a.modified < %s
order by a.`name`, b.`name`
limit %s,%s""", (from_date, to_date, int(limit_start), int(limit_page_length)), as_dict=True)
    return get_response(datalist)

    
@frappe.whitelist()
def get_purchaseorder(from_date=None, to_date=None, limit_start=None, limit_page_length=None):
    if not limit_page_length:
        limit_page_length = 20
    if not limit_start:
        limit_start = 0 
    datalist = frappe.db.sql("""SELECT 
concat(a.`name`,'-',b.`name`) id   
, a.`name` po_number
, a.company
, a.schedule_date po_date
, a.title account_name
, c.`name` account_code
, b.item_code
, b.item_name   
, b.qty
, b.uom
, b.rate unit_price
, b.amount
, a.currency
, b.total_weight net_weight
, a.modified
, a.docstatus
, b.bom
FROM `tabPurchase Order` a
JOIN `tabPurchase Order Item` b ON a.`name` = b.`parent` AND b.`parenttype` = 'Purchase Order'
JOIN `tabSupplier` c ON a.title = c.`name`
WHERE a.modified >= %s and a.modified < %s
order by a.`name`, b.`name`
limit %s,%s""", (from_date, to_date, int(limit_start), int(limit_page_length)), as_dict=True)
    return get_response(datalist)

@frappe.whitelist()
def get_warehouse(from_date=None, to_date=None, limit_start=None, limit_page_length=None):
    if not limit_page_length:
        limit_page_length = 20
    if not limit_start:
        limit_start = 0 
    datalist = frappe.db.sql("""select name as `Code`
, warehouse_name as `Description`
, type as `Type`
from tabWarehouse
order by `name`
limit %s,%s""", (int(limit_start), int(limit_page_length)), as_dict=True)
    return get_response(datalist)

def get_response(datalist):
    frappe.local.response.update({
        "data":  datalist})
    return build_response("json")