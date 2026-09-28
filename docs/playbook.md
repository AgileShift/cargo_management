# QuickBox - Flujos Ideales - Crear PlayBook

## Flujos

### Flujos de Facturaciones

1. Cuando el cliente se compra
2. Cuando le compramos(Online) al cliente
   - Flujo de Compras(Por verse)
3. Cierre de caja de facturas del dia?

### Flujo de Regla de Precios

1. Separar por servicios
2. Tabla de Costos por Tarjetas

### Flujo de Entregas

1. Cuando el cliente retira en local(Sin importar la forma de pago)
2. Cuando es via delivery Local:
   - Cuando El mensajero recibe efectivo
3. Cierre de caja de entregas del dia?

### Flujo de Soporte

1. Incidencias cuando el cliente se compra
2. Incidencias cuando el nosotros le compramos al cliente
3. Esto va relacionado con el flujo de terminos y condiciones

### Flujo de Caja

1. Pago Total
2. Pago Total + Adelanto
3. Pago Parcial + Pago anterior(Adelanto)
4. Pagos con Tarjeta:
   - Activar Reglas de Precios
   - Tabla de Comisiones
   - Pagos al contado o pagos con financiamientos

### Flujo de Reporte Operativo

1. Paquetes Rezagados, Atrasados
2. Compras Rezagados, Atrasados
3. Soportes pendientes
4. Notificaciones via CRON(Definir medios)?

### Flujo de Terminos, Politicas y Condiciones

1. Determinadas por el tipo de facturacion
2. Determinada por el tipo de tienda o transportista?

### Flujo de Facturación de Membresias\Servicios

Relacionado con Flujo Terminos y Politicas(Mostrar claramente los terminos)

Relacionado con Flujo de Pagos(Impresion de Recibos)

1. Servicio de Seguros x Producto o Envio
2. Servicio de Libras Prepagadas
3. Membresia para tarifas preferenciales o Deliverys x mes
4. Membresia para envios con seguros
5. Membresia para creditos?
6. Acumulacion de Puntos o Tarjeta acumulable fisica con CODIGO

### Flujo de Notificaciones automaticas al cliente? - (Puede revelar incosistencias)

### Flujo de Creditos

1. Sistema de creditos en importaciones
2. Sistema de Creditos en Ordenes de Venta(Asistencia)
3. Tarifas segun creditos

## Modulo de compra

- QuickBox Nicaragua compra al proveedor el producto solicitado por nuestro cliente.

### Flujo de trabajo cuando nosotros realizamos la compra del producto por el cliente

1. Se realiza la cotización:
   - El cliente envía distintos enlaces y con respecto a eso le brindamos la cotización
2. Se realiza la venta al cliente(Sales Order):
   - Convertir la cotización en una orden de venta
3. Se recibe un adelanto(Payment Entry) o se financia:
   - El cliente realiza un depósito en nuestra cuenta de banco por un monto establecido para realizar su compra.(Modulo de cuentas de bancos)
   - Si el cliente es de confianza, nosotros realizamos la compra sin solicitar un depósito.(Modul de credito)
4. Se realiza la orden al proveedor que nos brinda el cliente(Purchase Order):
   - El proveedor nos brinda un numero de rastreo que usamos para darle seguimiento al paquete.
   - Necesitamos darle seguimiento a la cuenta de banco con la que se realiza este pago al proveedor.(Modulo de cuentas de banco)
5. Se recibe el producto en almacén en USA:
   - El personal en USA sube el número de rastreo a un sistema de ellos y le llama “Warehouse Receipt”, esto se verifica manualmente por nosotros
   - Una hoja de entrada de inventario puede tener uno o muchos números de rastreo. (Modulo de Inventario)
6. Se transporte el producto desde USA hasta Nicaragua:
   - El personal en USA envía los paquetes hacia Nicaragua y sube un registro al sistema de ellos, en el cual nosotros verificamos manualmente
   - Con el registro de exportación podemos brindar una fecha aproximada de entrega al cliente en Nicaragua(Modulo de Venta)
7. Se reciben los paquetes en Oficina:
   - Se procede a realizar un inventario de recepción
   - Se notifica al cliente cuando los paquetes están en nuestra oficina:
     - Si se necesita se solicita una factura de la compra del cliente para brindarle el valor de importación.
   - El cliente puede solicitar retirar el paquete personalmente o solicitar un envio hasta su casa por un cargo extra:
     - En caso de solicitar envío, programamos una entrega(Delivery Note) con un mensajero externo(Necesitamos una hoja de ruta) y se realiza un cobro adicional(Modulo de entregas)
   - El cliente puede pagar en efectivo o transferencia(Payment Entry):
     - Este pago se debe de registrar ya que puede realizar pagos parciales con diferentes métodos para completar el pago de su factura(Modulo cuenta de bancos)

### Flujo de trabajo cuando solo importamos la paqueteria

1. El cliente nos envia el numero de rastreo que le brindó su proveedor:
   - El número se registra en nuestro sistema(Parcel)
   - Le podemos dar seguimiento al paquete y generar "Alertas" en ciertos eventos:
     1. Paquete se entrego(Modulo de inventario)
     2. Paquete se retraso
     3. Paquete fue firmado por alguien fuera de nuestro personal
   - Se repiten todos los pasos del flujo "cuando nosotros realizamos la compra" desde el paso 5 hasta el último paso.

### Flujo de trabajo cuando vendemos los productos

1. Se repiten todos los pasos del flujo "cuando nosotros realizamos la compra" desde el paso 4 hasta el paso 6
2. Se realiza una orden de venta al cliente
3. Se realiza una factura
4. Se agenda una entrega(Cliente paga al momento de la entrega)
5. Inventario disminuye de inmediato

---

## Modulo de Entregas

- Hoja de entregas por dia y hora
- Crear una hoja de ruta de los clientes marcados como envio por delivery

## Modulo de cuentas de banco <- Modulo de Ventas

- Arqueos
- Registro de pagos de clientes y a proveedores
- Reporte

## Modulo de credito a cliente

- Manejo de cartera de clientes con credito abierto

### Flujo

- Manejo de clientes y cuentas por cobrar
- Verficacion de limite de credito
- Alerta de incumplimiento cada 24 horas luego de 5 dias
- Aplicar regla de seguridad, luego de Y incumplimientos se negara el credito al cliente por un periodo de tiempo X

## Modulo de Inventario

- Ingreso, control y salida de mercaderia
- Alerta de mercaderia de cliente con X dias de NO ENTREGA

### Los siguientes procesos deberán ser automatizados

Al recibir la carga en oficina(de manera semanal), tenemos que registrar una entrada a bodega:

- Se escanea cada número de rastreo
- Se pesa cada paquete
- Se procede a realizar la factura al cliente:
  - Una factura puede contener el servicio de importacion de 1 o varios paquetes
- Se procede a notificar al cliente

### Solucion

Una pantalla que permite precargar todos los paquetes que existen en una "hoja de movimiento de bodega"(USA a Nicaragua).

En esta pantalla se agrega rápidamente: el peso y el valor de factura de cada paquete, Una vez terminado de inventariar toda la paquetería se guarda esta "hoja de recepción" y se generan automáticamente las facturas y se le notifica al cliente: vía correo o vía SMS

## Modulo de rastreo

- Seleccion de producto a rastreas, cada producto(compra a cliente) ya debe tener su TrackingID correspondiente.
- Alertas
  - Entrega
  - Extravio
  - Paquete fue firmado por alguien fuera de nuestro personal
  - Retraso
  - ...

Le damos seguimiento a los paquetes con los números de rastreo(Esto nos permite accionar antes que pase demasiado tiempo):

- actualmente el seguimiento es manual y genera mucho trabajo al personal

Usaremos el API de EasyPost(Tracking)

Bajo ciertos eventos un paquete debe de ser alertado directamente a nuestro personal y al cliente:

- El paquete falla al ser entregado
- El paquete es recibido(Firmado) por una persona ajena a nuestro personal
- El paquete no logro ser entregado por que la entrega se realiza fuera de horario de oficina
- El paquete no logró ser entregado y se reagendara para el siguiente dia habil
- El paquete no logró ser entregado y se necesita que alguien reagende la entrega, de lo contrario aparece para que se retire en las oficinas de la empresa de envíos.
- El paquete sufrió un retraso
- El paquete ha sido entregado:
  - Solicitamos al cliente nos brinde máximo 24 horas para que confirmemos la recepción:
    - 24 horas es el tiempo en que el personal en Miami demora en subir los paquetes a su sistema y así nosotros confirmar la recepción.
    - Si han pasado más de 24 horas y aun no aparece en el sistema de Miami se genera una alerta para realizar una solicitud directamente al personal de Miami. Así de esa manera confirmar la recepción pronta o decirle al cliente que su paquete fue entregado incorrectamente.
- Cuando un paquete aparece como despachado de Miami(Ellos nos brindan una hoja de salida), notificar al cliente una fecha próxima de entrega

### Los clientes solicitan actualizaciones sobre sus paquetes muchas veces al día

**Solución:**

Brindarle un código a cada cliente que permita

Que inicie sesión y pueda ejecutar las siguientes acciones:

- Verificar el estado de sus paquetes:
  - Solicitar más información si un paquete sobrepasa las 24 horas y sigue sin aparecer:
    - Esto enviaría una alerta al personal para que se comuniquen directamente con el cliente.
- Reportar números de rastreo de sus proveedores
- Ver sus facturas pendientes:
  - Subir un comprobante de pago(la foto de un voucher)
- Ver su historial de facturas
- Realizar una solicitud de compra de productos:
  - Cuando esta solicitud es atendida se envía una alerta al cliente, si la aprueba, se procede con el flujo de compra anteriormente descrito.
- Historial de incidencias

---

Necesitaremos desarrollador los siguientes módulos para mejorar la atención al cliente

## Módulo de incidencias

- incidencia cuando un paquete llegue a nombre incorrecto( no usen su código de cliente)
- Incidencia cuando un paquete nos llegue en malas condiciones
- Incidencia cuando un paquete nos llegue con productos faltantes o en mal estado
- Resolucion de incidencias

Este módulo de incidencia nos debe de permitir generar un reembolso al cliente en caso de ganar la incidencia o notificarle de otro tipo de resolución

### Ejemplo

- si un paquete llega a nombre incorrecto se genera un cobro de $5, se le debe de notificar al cliente si desea importarlo y pagar el extra o enviar a alguien al almacén a retirarlo
- Si un paquete llega a nosotros y sus productos se encuentran en mal estado. O Si un paquete muestra que fue entregado pero aparece firmado por otra persona o el paquete muestra que fue entregado y realmente no lo tenemos en USA::
  - Si nosotros compramos, tenemos que contactarnos con el proveedor para gestionar una garantía
  - Si el cliente se compró, le apoyamos al cliente a gestionar
- Si un paquete es dañado al transportarlo:
  - Generamos la incidencia para proceder a reembolsar al cliente por su compra
- Si un paquete es extraviado en nuestro almacén o transporte
  - Generamos la incidencia para proceder a reembolsar al cliente

---

## Modulo de Firma digital

A los clientes se les hara firmar un contrato de servicio, donde se declarara:

- Paquetes que lleguen a nombre incorrecto
  - Cobro extra, más la espera no estimada
  - O que los lleguen a retirar
- Metodo de trabajo
- Tarifas
  - Detalle más variaciones
- Tiempos
  - Retrasos
- Reclamos y garantias:
  - No garantía en caso de mal embalaje del proveedor
  - No garantía para monitores usados
- Reporte de facturas en casos de electronicos
  - Que pasa si la factura es alterada

## Módulo Reporte

De manera manual encontramos a los clientes que solían ser recurrentes y perdieron la Constancia para contactarlos y activarlos nuevamente, necesitamos una manera rápida de generar un reporte de estos clientes:

- Más activos( de 3 a más )
- Menos activos(1)
- Nuevos
- Cero actividad

Reporte de ventas

Reporte de ganancia por cada traslado de mercancía

Reporte de clientes solicitando envíos locales y su gasto

## Politicas

1. Variacion de precio si la carga es retenida.
   - Las cotizaciones pueden variar de precio en caso de retencion.
2. Las tarifas son de referencia, para obtener un valor aproximado de importac
   - Sin embargo aduana puede ajustar el valor de impuestos por tu compra.
3. Que no transportamos
   - Que paso si lo envias
4. Que pasa si no retira
   - Cobro de Almacenamiento
5. Somos un Gestor Logistico no una agencia aduanera
6.

## Addons

1. Seguro:
   - Definir proceso para la reclamacion.
   - Se invlida si no se demuestra que se nos entrego
   - Que compras no aseguramos

## Funcionalides

Aviso de avance en caso de retencion

Aviso de retiro

Aviso de multa por no retiro

---

## La cotizadora de precios(Top Prioridad)

Deberia de enviar el costo de precio por libra al dia

por el peso aproximado que proveyeron y el valor aproximado de calzar todo

de lo contrario el cambio seria al momento del pesaje final en DESTINO(MGA)

Para eso necesitamos el documento de rutas, y tarifarios :D??

---

## Rating sobre el shipper

Que los clientes puedan dar rating sobre el shipper

Ofrecer algun tipo de programa de puntos sobre las califaciones si se hacen publicas.

Por ejemplo, Despues de recibida su compra

Darle la opcionde valorar:

1. La traida, el servicio
2. El shipper, como le salio su compra
   - Esto generaria:
     1. Valorar Shipper
     2. Valorar Producto en detalle
