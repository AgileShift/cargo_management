Hola {{ doc.customer_name }}!

El transportista nos indica que tu paquete: {{ doc.tracking_number }} ha sido entregado.

Espera 24 horas habiles para que el almacen en Miami lo procese y verifique.<br>
Recibiras un correo de confirmacion una vez tengamos el paquete.

Una vez te brindemos el confirmado, te brindaremos la fecha de entrega estimada en Nicaragua.

<ul>
    <li>Paquete: {{ doc.tracking_number }}</li>
    <li>Transportista: {{ doc.carrier }}</li>
</ul>

Saludos, <br>
QuickBox Nicaragua
