frappe.ui.form.on("Sales Invoice", {

	refresh(frm) {

		// Show Message on Advances
		(frm.doc.advances || []).forEach((adv) => {

			frm.layout.show_message(`
				<div>
					Credito: <a href="/app/payment-entry/${adv.reference_name}">${adv.reference_name}</a> <br/>
					Monto sin asignar: <b>${frappe.format(adv.advance_amount, {fieldtype: "Currency"}, {only_value: true})}</b> <br/>
					<br/>
					Asignado a esta factura: <b>${frappe.format(adv.allocated_amount, {fieldtype: "Currency"}, {only_value: true})}</b>
				</div>`, 'blue', true
			);

		});

	},

});
