import PaymentService from '../services/payment_service.js';

/**
 * Called when a ride is completed to process the fare
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 * @returns {void}
 */
export async function initiatePaymentHandler(req, res) {
  try {
    // TODO: Validate request payload
    // TODO: Implement authentication and authorization checks
    const { rideId, fare } = req.body;

    // TODO: Ensure necessary business logic is handled before initiating payment
    const paymentResult = await PaymentService.initiatePayment(rideId, fare);

    res.status(200).json({
      success: true,
      data: paymentResult
    });
  } catch (error) {
    // TODO: Introduce more granular error handling as needed
    console.error('Error in initiatePaymentHandler:', error);
    res.status(500).json({
      success: false,
      message: 'An error occurred while initiating the payment'
    });
  }
}

/**
 * Returns transaction data for a specific ride
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 * @returns {void}
 */
export async function fetchPaymentDetailsHandler(req, res) {
  try {
    // TODO: Validate request parameters
    // TODO: Implement authentication and authorization checks
    const { rideId } = req.params;

    const paymentDetails = await PaymentService.getPaymentDetails(rideId);

    res.status(200).json({
      success: true,
      data: paymentDetails
    });
  } catch (error) {
    // TODO: Introduce more granular error handling as needed
    console.error('Error in fetchPaymentDetailsHandler:', error);
    res.status(500).json({
      success: false,
      message: 'An error occurred while retrieving payment details'
    });
  }
}