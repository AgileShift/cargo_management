# QuickBox Functional Playbook

Este documento conserva y organiza la visión funcional definida originalmente en **QuickBox - Flujos Ideales - Crear PlayBook** (2019).

No describe por sí solo el comportamiento actual de la aplicación ni establece políticas comerciales. Su propósito es preservar el modelo deseado, sus procesos, entradas y resultados esperados para derivar y revisar el [backlog funcional](functional-backlog.md).

## Clasificación del contenido

- **Operación confirmada:** ocurre actualmente.
- **Modelo esperado:** describe cómo debería funcionar integralmente.
- **Decisión pendiente:** requiere una definición comercial u operativa.
- **Referencia histórica:** conserva una idea o regla del documento de 2019 sin declararla vigente.

<a id="imp-01"></a>

## IMP-01 · Importación realizada por el cliente

**Clasificación:** operación confirmada y modelo esperado.

### Objetivo

Importar un paquete comprado directamente por el cliente y mantener su trazabilidad desde el número de rastreo hasta el retiro o la entrega.

### Entrada

- Número de rastreo proporcionado por el cliente.
- Cliente, servicio de transporte y descripción del paquete.

### Proceso

1. El número de rastreo se registra en `Parcel`.
2. Se da seguimiento externo al paquete.
3. En **Origen**, el paquete se confirma mediante `Warehouse Receipt` y se incorpora a un `Cargo Shipment`.
4. En **Destino**, la carga se recibe mediante `Cargo Shipment Receipt`.
5. Se pesan, rotulan y clasifican los paquetes.
6. Se genera la factura de importación.
7. El cliente paga y solicita retiro o entrega.

### Salidas

- Paquete relacionado con su cliente.
- Historial logístico.
- `Sales Invoice` por los servicios prestados.
- Pago, retiro o entrega.

### Eventos que requieren seguimiento

- El paquete fue entregado por el transportista.
- El paquete sufrió un retraso.
- El paquete fue firmado por una persona ajena al personal de Origen.
- La entrega falló, fue reagendada, quedó disponible para retiro o fue devuelta.

<a id="asc-01"></a>

## ASC-01 · Asistencia de compra

**Clasificación:** operación confirmada y modelo esperado.

QuickBox compra al proveedor el producto solicitado por el cliente. El proceso comercial existe actualmente; su trazabilidad integral entre documentos continúa siendo el modelo funcional esperado.

### Entrada

- Enlaces de los productos.
- Talla, color, cantidad y demás variantes necesarias.
- Datos del cliente.
- Cotización aprobada.
- Adelanto confirmado o crédito autorizado.

### Proceso comercial confirmado

1. El cliente envía los enlaces de los productos.
2. Se prepara la cotización.
3. Se confirma la compra con el cliente.
4. Se recibe el adelanto acordado o se autoriza el crédito.
5. QuickBox realiza la compra.
6. Se obtiene el número de rastreo y se registra el paquete.
7. El paquete continúa por el flujo logístico ordinario.

### Modelo documental esperado

1. Preparar una `Quotation`.
2. Convertir la cotización aprobada en `Sales Order`.
3. Registrar el adelanto mediante `Payment Entry` o aplicar el crédito autorizado.
4. Registrar la compra al proveedor mediante `Purchase Order`.
5. Relacionar el número de rastreo y el `Parcel` con la asistencia de compra.
6. Procesar el paquete en Origen y Destino.
7. Generar la `Sales Invoice` correspondiente.
8. Registrar el saldo restante.
9. Completar el retiro o la entrega.

### Base técnica parcial

- `Parcel` identifica si se trata de una compra asistida.
- `Parcel` puede relacionarse con una `Sales Order`.
- Los ítems de venta pueden relacionarse con un `Parcel`.
- Estas relaciones no demuestran por sí solas que la cotización, el adelanto, la compra al proveedor y la facturación estén conectados automáticamente de principio a fin.

### Salidas

- Compra aprobada y realizada.
- Adelanto o crédito registrado.
- Compra al proveedor.
- Paquete y número de rastreo relacionados.
- Facturación de los productos y servicios.
- Saldo final y entrega.

### Decisiones pendientes

- Documento autoritativo para iniciar la solicitud.
- Condiciones para comprar sin adelanto.
- Relación contable y documental con la compra al proveedor.
- Momento y documento de cierre de la asistencia.

<a id="log-01"></a>

## LOG-01 · Logística en Origen y Destino

**Clasificación:** operación confirmada.

> **Texto original de 2019:** “Se recibe el producto en almacén en USA” y “Se transporta el producto desde USA hasta Nicaragua”.

El modelo vigente utiliza los conceptos **Origen** y **Destino**. Una operación puede tener ubicaciones diferentes sin cambiar su flujo funcional.

### Origen

1. El paquete se recibe y verifica mediante `Warehouse Receipt`.
2. Un recibo puede contener uno o varios números de rastreo.
3. Los recibos se agregan al `Cargo Shipment`.
4. La carga se prepara y sale desde Origen.

### Destino

1. Se recibe el `Cargo Shipment` mediante `Cargo Shipment Receipt`.
2. Se realiza el inventario de recepción.
3. Los paquetes se pesan, rotulan y clasifican.
4. Las facturas se generan desde la recepción.
5. Las tarifas y descripciones se revisan manualmente antes de continuar con el cobro.

### Automatización de la recepción

> **Texto original de 2019:** “Una pantalla que permite precargar todos los paquetes que existen en una hoja de movimiento de bodega. En esta pantalla se agrega rápidamente el peso y el valor de factura de cada paquete; una vez terminado de inventariar toda la paquetería se guarda esta hoja de recepción y se generan automáticamente las facturas”.

Parte de este modelo existe actualmente mediante `Cargo Shipment Receipt`: carga los paquetes relacionados, permite procesar su información y genera las facturas. Continúa pendiente evaluar cualquier necesidad adicional de automatización o notificación.

### Salidas

- Recepción confirmada en Origen.
- Embarque preparado.
- Recepción confirmada en Destino.
- Paquetes pesados, rotulados y clasificados.
- Facturas generadas y revisadas.

<a id="fac-01"></a>

## FAC-01 · Facturación y precios

**Clasificación:** operación confirmada, modelo esperado y decisiones pendientes.

### Escenarios de facturación

1. Importación realizada por el cliente.
2. Asistencia de compra.
3. Venta de productos.
4. Servicios adicionales aprobados.

### Venta de productos

El documento original propone este flujo:

1. Registrar la compra al proveedor.
2. Recibir y trasladar los productos.
3. Crear la `Sales Order` del cliente.
4. Generar la `Sales Invoice`.
5. Programar la entrega cuando corresponda.
6. Disminuir el inventario conforme al documento de entrega o venta aplicable.

### Modelo esperado

- Una factura puede incluir el servicio de importación de uno o varios paquetes.
- Las reglas de precios deben distinguir los servicios.
- La estimación debe conservar los datos utilizados para calcularla.
- El valor definitivo puede ajustarse con el peso y las condiciones confirmadas en Destino.

### Cotizador

> **Texto original de 2019:** “La cotizadora de precios (Top Prioridad) debería de enviar el costo de precio por libra al día por el peso aproximado que proveyeron y el valor aproximado de calzar todo; de lo contrario el cambio sería al momento del pesaje final en DESTINO (MGA)”.

Se conserva como modelo esperado. Las fórmulas, rutas, tarifas, mínimos, impuestos, vigencia de la cotización y ajustes aduaneros requieren definición antes de implementarse.

### Decisiones pendientes

- Reglas de precio por servicio.
- Tabla de comisiones por pagos con tarjeta.
- Tratamiento de pagos de contado y financiamientos.
- Variaciones por retención o ajustes aduaneros.
- Datos y vigencia de las cotizaciones.

<a id="pag-01"></a>

## PAG-01 · Pagos, adelantos y crédito

**Clasificación:** operación confirmada, modelo esperado y decisiones pendientes.

### Escenarios de pago

1. Pago total.
2. Pago total utilizando un adelanto anterior.
3. Pago parcial y aplicación de un adelanto.
4. Pagos con diferentes métodos.
5. Pagos con tarjeta.
6. Crédito autorizado.

### Modelo esperado

- Registrar cobros de clientes y pagos a proveedores.
- Relacionar los pagos con sus documentos correspondientes.
- Permitir pagos parciales mediante diferentes métodos hasta completar la factura.
- Conservar controles de caja y bancos sin duplicar los documentos contables.
- Contar con cierres diarios para la facturación y las entregas, relacionados con los documentos que originaron cada cobro.

### Crédito

- Manejar clientes y cuentas por cobrar.
- Verificar el límite disponible antes de autorizar una operación.
- Alertar sobre incumplimientos.
- Aplicar restricciones únicamente conforme a reglas aprobadas.

> **Texto original de 2019:** “Alerta de incumplimiento cada 24 horas luego de 5 días” y “luego de Y incumplimientos se negará el crédito al cliente por un periodo de tiempo X”.

Los plazos, cantidades de incumplimientos, restricciones y autoridades de aprobación continúan como decisiones comerciales pendientes.

### Salidas

- Pago o adelanto registrado.
- Saldo actualizado.
- Crédito evaluado.
- Operación autorizada o remitida a revisión.

<a id="ent-01"></a>

## ENT-01 · Retiros y entregas

**Clasificación:** operación confirmada y modelo esperado.

### Escenarios

1. El cliente retira en el local, sin importar la forma de pago.
2. El cliente solicita una entrega local.
3. El mensajero recibe efectivo o entrega vuelto.
4. El cliente solicita una entrega nacional.

### Modelo esperado

- Crear una hoja de entregas por día y hora.
- Generar una ruta para los clientes marcados para entrega.
- Agrupar paquetes listos.
- Asignar responsable.
- Registrar el monto por cobrar y el vuelto que debe llevarse.
- Registrar el resultado de cada entrega.

### Salidas

- Retiro confirmado.
- Entrega programada.
- Ruta preparada.
- Cobro y resultado conciliados.

### Decisiones pendientes

- Programación y asignación.
- Intentos fallidos.
- Evidencia de entrega.
- Cierre y liquidación con mensajeros.

<a id="seg-01"></a>

## SEG-01 · Seguimiento y excepciones del transportista

**Clasificación:** operación confirmada y modelo esperado.

El seguimiento externo es un proceso lateral al ciclo logístico del `Parcel`. EasyPost y 17Track ya proporcionan integraciones para recibir información del transportista.

> **Texto original de 2019:** “Usaremos el API de EasyPost (Tracking)”.

EasyPost ya no es únicamente una propuesta futura. El modelo esperado es normalizar los eventos recibidos y convertir únicamente las excepciones válidas en acciones para el personal.

> **Texto original de 2019:** “Actualmente el seguimiento es manual y genera mucho trabajo al personal”.

Las integraciones reducen parte de la consulta manual, pero no demuestran que el seguimiento y la resolución de todas las excepciones estén automatizados.

### Eventos contemplados

- Entrega fallida.
- Firma por una persona ajena al personal de Origen.
- Intento fuera del horario de atención.
- Entrega reagendada.
- Paquete disponible para retiro.
- Retraso.
- Devolución al remitente.
- Marcado como entregado, pero aún no confirmado en `Warehouse Receipt`.
- Salida desde Origen.

### Confirmación posterior a la entrega del transportista

> **Texto original de 2019:** “Solicitamos al cliente nos brinde máximo 24 horas para que confirmemos la recepción” y “si han pasado más de 24 horas y aún no aparece en el sistema de Miami se genera una alerta”.

El tiempo de espera, el calendario de atención, los destinatarios de la alerta y las reglas de escalamiento deben definirse. La ausencia de confirmación no debe interpretarse automáticamente como extravío.

### Salidas

- Estado externo actualizado.
- Excepción identificada.
- Seguimiento asignado.
- Resolución documentada.

<a id="not-01"></a>

## NOT-01 · Notificaciones automáticas

**Clasificación:** modelo esperado y decisión pendiente.

El documento de 2019 propone notificaciones al personal y al cliente para eventos como:

- recepción confirmada;
- salida desde Origen;
- retraso;
- llegada a Destino;
- facturación;
- pago;
- disponibilidad para retiro o entrega;
- avance cuando exista una retención;
- cargos o medidas aprobadas por falta de retiro;
- incidencias y resoluciones.

Las notificaciones deben enviarse solamente después de validar el evento correspondiente.

### Decisiones pendientes

- Eventos que generan notificaciones.
- Destinatarios.
- Canales.
- Plantillas.
- Reintentos.
- Preferencias del cliente.
- Protección contra mensajes prematuros o duplicados.

<a id="inc-01"></a>

## INC-01 · Incidencias, reclamaciones y resoluciones

**Clasificación:** modelo esperado y decisiones pendientes.

### Casos contemplados

- Paquete recibido con nombre incorrecto.
- Paquete recibido en malas condiciones.
- Productos faltantes o dañados.
- Paquete marcado como entregado, pero no confirmado en Origen.
- Cambio del servicio de transporte.
- Daño o extravío durante el traslado.

### Modelo esperado

1. Registrar la incidencia contra el paquete.
2. Reunir evidencia.
3. Asignar seguimiento.
4. Investigar el caso.
5. Registrar la decisión.
6. Relacionar cualquier resolución aprobada.
7. Comunicar el resultado.

### Responsabilidad según el origen de la compra

- Si QuickBox realizó la compra, debe gestionarse el caso con el proveedor.
- Si el cliente realizó la compra, QuickBox puede apoyarlo en la gestión.

### Valores y resoluciones históricas

> **Texto original de 2019:** “Si un paquete llega a nombre incorrecto se genera un cobro de $5”.

El cobro se conserva únicamente como referencia histórica. Su existencia, monto, condiciones y autorización requieren una decisión comercial vigente.

> **Texto original de 2019:** “Si un paquete es dañado o extraviado en nuestro almacén o transporte, generamos la incidencia para proceder a reembolsar al cliente”.

La incidencia debe permitir registrar la investigación y una resolución aprobada. No se debe prometer automáticamente un reembolso sin definir responsabilidad, evidencia, cobertura y autoridad de aprobación.

<a id="por-01"></a>

## POR-01 · Portal y autoservicio del cliente

**Clasificación:** modelo esperado.

El documento original propone que el cliente pueda:

- iniciar sesión;
- consultar el estado de sus paquetes;
- solicitar información adicional;
- reportar números de rastreo;
- consultar facturas pendientes;
- subir comprobantes de pago;
- consultar su historial de facturas;
- solicitar una asistencia de compra;
- aprobar una solicitud atendida;
- consultar su historial de incidencias.

### Entradas

- Identidad del cliente.
- Paquetes, ventas, facturas, pagos e incidencias relacionados.

### Salidas

- Solicitudes registradas.
- Evidencia adjunta.
- Información consultada conforme a permisos.
- Acciones remitidas al flujo correspondiente.

### Decisiones pendientes

- Autenticación.
- Información visible.
- Permisos.
- Acciones permitidas.
- Controles de revisión.
- Relación con futuras aplicaciones de comercio electrónico.

<a id="inv-01"></a>

## INV-01 · Inventario y almacenamiento

**Clasificación:** operación confirmada, modelo esperado y decisiones pendientes.

### Capacidades

- Ingreso, control y salida de mercadería.
- Recepción y clasificación de paquetes.
- Identificación de paquetes pendientes de retiro.
- Alertas sobre paquetes almacenados durante un período definido.

> **Texto original de 2019:** “Alerta de mercadería de cliente con X días de no entrega”.

El período gratuito, los cargos, la secuencia de avisos, las excepciones y el tratamiento de paquetes abandonados requieren definición comercial y revisión legal.

<a id="ser-01"></a>

## SER-01 · Servicios adicionales

**Clasificación:** referencia histórica y decisiones pendientes.

El documento de 2019 contempla:

- seguro por producto o envío;
- libras prepagadas;
- membresías con tarifas preferenciales;
- membresías con entregas incluidas;
- membresías con seguro;
- membresías relacionadas con crédito;
- acumulación de puntos;
- calificación del servicio, transportista o producto.

No se consideran servicios aprobados hasta definir:

- productos ofrecidos;
- precio;
- cobertura;
- exclusiones;
- vencimiento;
- transferibilidad;
- reclamaciones;
- tratamiento contable.

### Garantías históricas

> **Texto original de 2019:** “No garantía en caso de mal embalaje del proveedor” y “No garantía para monitores usados”.

Estas frases se conservan como referencia histórica. Cualquier exclusión de responsabilidad o garantía requiere política aprobada y revisión legal.

### Calificaciones

El modelo contempla que, después de recibir la compra, el cliente pueda valorar:

1. El servicio de importación.
2. El proveedor o `Shipper`.
3. El producto.

La visibilidad, moderación y cualquier incentivo por publicar calificaciones permanecen pendientes.

<a id="rep-01"></a>

## REP-01 · Reportes administrativos y operativos

**Clasificación:** modelo esperado.

### Reportes operativos

- Paquetes rezagados o atrasados.
- Compras rezagadas o atrasadas.
- Incidencias pendientes.
- Entregas locales.
- Paquetes pendientes de retiro.

### Reportes administrativos

- Facturas pendientes.
- Órdenes de importación pendientes de pago.
- Cierres de caja.
- Ventas.
- Ganancia por traslado de mercancía.
- Costos de entrega.
- Actividad de clientes:
  - más activos;
  - menos activos;
  - nuevos;
  - sin actividad.

Las métricas, fuentes contables, audiencias y períodos deben definirse antes de implementar cada reporte.

> **Texto original de 2019:** “De manera manual encontramos a los clientes que solían ser recurrentes y perdieron la constancia para contactarlos y activarlos nuevamente”.

Se conserva como necesidad de identificar cambios en la actividad de los clientes. La definición de cliente recurrente, inactivo o reactivable continúa pendiente.

<a id="pol-01"></a>

## POL-01 · Políticas, términos y decisiones pendientes

**Clasificación:** referencia histórica y decisiones pendientes.

El documento original identifica la necesidad de establecer términos y políticas según el servicio, la facturación y el transportista.

### Temas conservados

1. Variación del precio cuando una carga es retenida.
2. Tarifas utilizadas como referencia para una estimación.
3. Posibles ajustes de impuestos o aduana.
4. Productos que no se transportan.
5. Consecuencias de enviar un producto restringido.
6. Paquetes no retirados y posibles cargos de almacenamiento.
7. Alcance como gestor logístico.
8. Reclamaciones y seguros.
9. Reporte de facturas para artículos electrónicos.
10. Tratamiento de documentos alterados.
11. Contrato o aceptación digital de las condiciones del servicio.

Estos temas no constituyen políticas vigentes dentro de este Playbook. Cada uno requiere una definición aprobada en su documentación operativa o legal correspondiente.

## Contenido deliberadamente fuera de alcance

La visión histórica sobre fuerza laboral, control de asistencia y cálculo de planilla pertenece a Frappe HR y a la documentación laboral de Grupo Real. No forma parte del modelo funcional de `cargo_management`.
