# Copyright (c) 2026, Sooraj MS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class LibraryTransaction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		article: DF.Link
		date: DF.Date
		library_member: DF.Link
		type: DF.Literal["Issue", "Return"]
	# end: auto-generated types

	_DOCTYPE_NAME = "Library Transaction"

# check library member has a valid membership
	def validate_Membership(self):
		valid_membership = frappe.db.exists(
			"Library Membership",
			{
				"library_member":self.library_member,
				"docstatus" : DocStatus.submitted(),
				"from_date":("<",self.date),
				"to_date" : (">",self.date)
			},
		)
		if not valid_membership:
			frappe.throw("No Valid Membership Available")
# check article already issued
	def validate_Issue(self):
		self.validate_Membership()
		curr_article = frappe.get_doc("Article",self.article)

		if curr_article.status == "Issued":
			frappe.throw("Article is Already Issued to a Member.")

# check article already returned
	def validate_Return(self):
		self.validate_Membership()
		curr_article = frappe.get_doc("Article",self.article)

		if curr_article.status == "Available":
			frappe.throw("Article cannot be returned without being issued.")		

# Article Issue Limit
	def validate_max_limit(self):
		max_articles = frappe.get_single_value("Library Settings","max_articles")
		count = frappe.db.count(
			"Library Transaction",{
				"library_member" : self.library_member,
				"type": "Issue",
				"docstatus" : DocStatus.submitted()
			}
		)
		if count >= max_articles:
			frappe.throw("Article Issue limit reached.")

# Before Submit
	def before_submit(self):
		if self.type == "Issue":
			self.validate_Issue()
			curr_article = frappe.get_doc("Article",self.article)
			curr_article.status = "Issued"
			curr_article.save()
		elif self.type == "Return":
			self.validate_Return()
			curr_article = frappe.get_doc("Article",self.article)
			curr_article.status = "Available"
			curr_article.save()


