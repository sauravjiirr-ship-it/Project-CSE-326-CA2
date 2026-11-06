const vehicleType = document.querySelector('#vehicle-type');
const vehicleCards = document.querySelectorAll('.card');
const noVehicles = document.querySelector('#no-vehicles');
const bookingForm = document.querySelector('#booking-form');
const selectedVehicle = document.querySelector('#selected-vehicle');
const pickupDate = document.querySelector('#pickup-date');
const returnDate = document.querySelector('#return-date');
const rentalDays = document.querySelector('#rental-days');
const totalAmount = document.querySelector('#total-amount');
const confirmation = document.querySelector('#confirmation');
let selectedPrice = 0;

// Filter the vehicle cards by the type selected in the search form.
document.querySelector('#search-form').addEventListener('submit', function (event) {
  event.preventDefault();
  const type = vehicleType.value;
  let visibleCount = 0;
  vehicleCards.forEach(function (card) {
    const showCard = type === 'all' || card.dataset.type === type;
    card.hidden = !showCard;
    if (showCard) visibleCount += 1;
  });
  noVehicles.hidden = visibleCount > 0;
  document.querySelector('#vehicles').scrollIntoView({ behavior: 'smooth' });
});

// Select a vehicle and move the visitor to the booking form.
document.querySelectorAll('.book-button').forEach(function (button) {
  button.addEventListener('click', function () {
    selectedVehicle.value = button.dataset.name;
    selectedPrice = Number(button.dataset.price);
    updateTotal();
    document.querySelector('#booking').scrollIntoView({ behavior: 'smooth' });
  });
});

selectedVehicle.addEventListener('change', function () {
  const option = selectedVehicle.options[selectedVehicle.selectedIndex];
  selectedPrice = Number(option.dataset.price || 0);
  updateTotal();
});

function updateTotal() {
  let days = 1;
  if (pickupDate.value && returnDate.value) {
    const start = new Date(pickupDate.value + 'T00:00:00');
    const end = new Date(returnDate.value + 'T00:00:00');
    const difference = Math.ceil((end - start) / 86400000);
    if (difference > 0) days = difference;
  }
  rentalDays.value = days;
  totalAmount.value = '₹' + (days * selectedPrice).toLocaleString('en-IN');
}

pickupDate.addEventListener('change', updateTotal);
returnDate.addEventListener('change', updateTotal);

// Check the form and show a booking summary in this browser only.
bookingForm.addEventListener('submit', function (event) {
  event.preventDefault();
  if (!bookingForm.reportValidity()) return;
  if (new Date(returnDate.value + 'T00:00:00') < new Date(pickupDate.value + 'T00:00:00')) {
    returnDate.setCustomValidity('Return date must be the pickup date or later.');
    returnDate.reportValidity();
    returnDate.setCustomValidity('');
    return;
  }
  updateTotal();
  const bookingId = 'RE' + Math.floor(100000 + Math.random() * 900000);
  document.querySelector('#confirm-id').textContent = bookingId;
  document.querySelector('#confirm-name').textContent = document.querySelector('#customer-name').value.trim();
  document.querySelector('#confirm-phone').textContent = document.querySelector('#phone').value.trim();
  document.querySelector('#confirm-vehicle').textContent = selectedVehicle.value;
  document.querySelector('#confirm-pickup').textContent = pickupDate.value;
  document.querySelector('#confirm-return').textContent = returnDate.value;
  document.querySelector('#confirm-days').textContent = rentalDays.value;
  document.querySelector('#confirm-total').textContent = totalAmount.value;
  bookingForm.hidden = true;
  confirmation.hidden = false;
  confirmation.scrollIntoView({ behavior: 'smooth', block: 'center' });
});

document.querySelector('#new-booking').addEventListener('click', function () {
  bookingForm.reset();
  bookingForm.hidden = false;
  confirmation.hidden = true;
  selectedPrice = 0;
  rentalDays.value = 1;
  totalAmount.value = '₹0';
  document.querySelector('#booking').scrollIntoView({ behavior: 'smooth' });
});
