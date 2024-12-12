<?php 

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;

class SmsController extends AbstractController
{
    public $records;
    public $processdList;

    function __construct(){
        
        //$csvFilePath = 'data/contacts.csv';
        // readfile and place phone numbers in array and have records like
        $this->records = ['12345678', '987654321'];
    }

    /**
     * @Route("/send", name="send_sms", methods={"POST"})
     */
    #[Route('/send', name: 'send_sendSms')]
    public function sendSms(Request $request)
    {
        $phoneNumber = $request->request->get('phone_number');
        $message = $request->request->get('message');

        if (!$phoneNumber || !$message) {
            return new JsonResponse(['error' => 'Invalid parameters'], 400);
        }

        // Check for duplicates
        if ($this->isPhoneNumberProcessed($phoneNumber)) {
            return new JsonResponse(['error' => 'This phone number has already been processed.'], 400);
        }

        $this->sendSingleSms($phoneNumber, $message);

        // Mark phone number as processed
        $this->markPhoneNumberAsProcessed($phoneNumber);

        return new JsonResponse(['message' => 'SMS sent successfully']);
    }

    /**
     * @Route("/bulk", name="send_bulk_sms", methods={"POST"})
     */
    #[Route('/bulk', name: 'bulk_sendBulkSms')]
    public function sendBulkSms(Request $request)
    {
        $message = $request->request->get('message');
        $recipients = $request->request->get('recipients');

        if (!$message || !is_array($recipients)) {
            return new JsonResponse(['error' => 'Invalid parameters'], 400);
        }

        foreach ($recipients as $phoneNumber) {
            // Check for duplicates
            if ($this->isPhoneNumberProcessed($phoneNumber)) {
                continue;
            }

            $this->sendSingleSms($phoneNumber, $message);

            // Mark phone number as processed
            $this->markPhoneNumberAsProcessed($phoneNumber);
        }

        return new JsonResponse(['message' => 'Bulk SMS sent successfully']);
    }

    private function sendSingleSms($phoneNumber, $message)
    {
		try {
			//$api->sendSms($phoneNumber, $message)
			return true;
		} catch (\Exception $e) {
            // Handle exception (log or return error response)
        }
    }

    private function isPhoneNumberProcessed($phoneNumber)
    {
        if(in_array($phoneNumber, $this->processdList)){
            return true;
        }
        return false;
    }

    private function markPhoneNumberAsProcessed($phoneNumber)
    {
        array_push($this->processdList, $phoneNumber);
    }
}

?>