arrivalDateInput.bind('input', function () {

    let deliveryDateRange = getDeliveryDateRange(arrivalDateInput.val()); // Calculate delivery date based on arrival date

    productDeliveryDateText.text('Fecha estimada de entrega en Nic: Entre el ' + deliveryDateRange.nearest + ' y el ' + deliveryDateRange.largest);
});

// Helper
function getNextDepartureDate(arrivalDate) {
    const departureDay = 5;  // the Number: 5, represents the Friday(Day of the week, 1 to 7). The actual departure date
    let nextDepartureDate = new Date();
    let offset = 0;

    if (arrivalDate.getUTCDay() === 4 || arrivalDate.getUTCDay() === 5) {
        arrivalDate.setUTCDate(arrivalDate.getUTCDate() + 2); // If Thursday or Friday then we cannot guarantee a departure, we calculate the second closest departure date
        console.log(arrivalDate.getUTCDate());
    }

    nextDepartureDate.setUTCDate((arrivalDate.getUTCDate() + offset ) + (departureDay + 7 - arrivalDate.getUTCDay()) % 7);

    return nextDepartureDate;
}

// This function calculate the range of delivery date
function getDeliveryDateRange(arrivalDate) {

    // If we have the estimated arrival date, then we get the closest shipping date
    let nearestDepartureDay = getNextDepartureDate(new Date(arrivalDate));  // Getting the Nearest departure date based on the arrival date
    let nearestDeliveryDate = new Date();
    let largestDeliveryDate = new Date();

    nearestDeliveryDate.setDate(nearestDepartureDay.getDate() + 12);
    largestDeliveryDate.setDate(nearestDepartureDay.getDate() + 15);

    return {
        'nearestDepartureDay': nearestDepartureDay.toLocaleDateString('es-ES', DATEOPTIONS),
        'nearest': nearestDeliveryDate.toLocaleDateString('es-ES', DATEOPTIONS),
        'largest': largestDeliveryDate.toLocaleDateString('es-ES', DATEOPTIONS)
    }
}

function calculateProductImportPrice(importPriceType) {
    let importPrice = 0;

    // Calculate the productTotalValue
    let totalProductValue = parseFloat(importPrice) + parseFloat(productPriceInput.val());
    productTotalText.text('Valor de total del producto: $' + totalProductValue);
}
//197