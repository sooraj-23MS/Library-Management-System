# Copyright (c) 2026, Sooraj MS and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator


class Article(WebsiteGenerator):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		article_name: DF.Data
		author: DF.Data | None
		description: DF.TextEditor | None
		image: DF.AttachImage | None
		isbn: DF.Data | None
		published: DF.Check
		publisher: DF.Data | None
		route: DF.Data | None
		status: DF.Literal["Issued", "Available"]
	# end: auto-generated types

	_DOCTYPE_NAME = "Article"
