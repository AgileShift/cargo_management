from enum import StrEnum


class Status(StrEnum):
	""" Parcel Statuses """

	AWAITING_RECEIPT = 'Awaiting Receipt'
	AWAITING_CONFIRMATION = 'Awaiting Confirmation'
	IN_EXTRAORDINARY_CONFIRMATION = 'In Extraordinary Confirmation'  # FIXME: We can remove "IN"
	AWAITING_DEPARTURE = 'Awaiting Departure'
	IN_TRANSIT = 'In Transit'
	IN_CUSTOMS = 'In Customs'
	SORTING = 'Sorting'
	TO_BILL = 'To Bill'
	UNPAID = 'Unpaid'
	FOR_DELIVERY_OR_PICKUP = 'Delivery or Pickup'  # FIXME, we can make to DELIVERY_OR_PICKUP
	FINISHED = 'Finished'
	CANCELLED = 'Cancelled'
	NEVER_ARRIVED = 'Never Arrived'
	RETURNED_TO_SENDER = 'Returned to Sender'


class MessageColor(StrEnum):
	BLUE = 'blue'
	RED = 'red'
	GREEN = 'green'
	PURPLE = 'purple'
	PINK = 'pink'
	YELLOW = 'yellow'
	GRAY = 'gray'
	ORANGE = 'orange'


class StatusMessage(StrEnum):
	# Awaiting Receipt Explanations
	TRANSPORTATION_NOT_DELIVERED_YET = 'El transporte aún no ha entregado el paquete.'
	ESTIMATED_DELIVERY_DATE_TODAY = 'La fecha programada de entrega es hoy.'
	ESTIMATED_DELIVERY_DATE_TOMORROW = 'La fecha programada es mañana.'
	ESTIMATED_DELIVERY_DATE = 'La fecha programada es: [DATE]'
	DELAYED_DELIVERY_DATE = 'Esta retrasado. Debio de ser entregado el: [DATE]'
	NOT_DELIVERY_DATE_ESTIMATED = 'No se ha indicado una fecha de entrega estimada.'

	TRANSPORTATION_DELIVERED_DATE = 'El transporte indica que entregó: [DATE]'
	SIGNED_BY = 'Firmado por: [SIGNER]'
	HAS_BEEN_1_DAY = 'Ha pasado 1 día'
	HAS_BEEN_X_DAYS = 'Han pasado [DAYS] días'
	WAIT_FOR_24_HOURS_CONFIRMATION = 'Por favor espera 24 horas hábiles para que el almacén confirme la recepción.'
	TRANSPORTER_INDICATE_ESTIMATE_DELIVERY_DATE = 'El transportista índico una fecha de entrega aproximada: [DATE]'
	PACKAGE_IN_EXTRAORDINARY_REVISION = 'El paquete se encuentra siendo verificado de forma extraordinaria.'
	TRANSPORTER_DELIVERY_DATE = 'El transportista indica que entrego el paquete el: [DATE].'
	NO_CARGO_SHIPPING = 'No hay envio de carga'
	PACKAGE_IN_TRANSIT_TO_DESTINATION = 'El paquete esta en transito a destino.'
	DEPARTURE_DATE = 'Fecha de despacho: [DATE]'
	ESTIMATED_RECEPTION_DATE = 'Fecha esperada de recepcion en Managua: [DATE]'
	CARGO_SHIPMENT = 'Embarque: [SHIPMENT]'
	PACKAGE_IN_CUSTOMS = 'El paquete se encuentra en proceso de desaduanaje.'
	PACKAGE_IN_OFFICE_SORTING = 'El paquete se encuentra siendo clasificado en oficina.'
	PACKAGE_READY = 'El paquete esta listo para ser retirado.'
	PACKAGE_FINISHED = 'Paquete Finalizado.'
	CONTACT_AGENT_FOR_PACKAGE_INFO = 'Contáctese con un agente para obtener mayor información del paquete.'
	PACKAGE_NEVER_ARRIVED = 'El paquete no llego al almacén.'
	PACKAGE_RETURNED = 'El paquete fue devuelto por el transportista al vendedor.'
	CONTACT_FOR_MORE_INFO = 'Contáctese con su vendedor y/o transportista para obtener mayor información.'

	CONTACT_YOUR_PROVIDER_FOR_INFO = 'Contacte a su proveedor para obtener mas información.'
