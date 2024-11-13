import streamlit as st


class Prompt:
    def get_travel_prompts(self, origin, destination, selected_preference):
        prompt = f""""
            step 1: Imagine a you are intelligent travel advisor helping me plan a trip from {origin} to {destination}.
            step 2: If given {origin} or {destination} does not exist then give message: Does not exist.
            step 3:
                task1: check what are travel options available for given {origin} and {destination}.
                task2: from available travel option suggest the most suitable correct transportation options with existing routes travel options with names and timing with distance"

            step 4: If direct path is not available from existing {origin} to {destination} tell travel option available to nearest place and from there to existing {destination} based on {selected_preference}"
            step 5: tell total time,cost with distance
            step 6: Change the answer format based on {selected_preference}

            Lets start :
            Question : What are the travel options available from 'Fake' to 'London'  ?
            2 :Fake is not available
            Answer:  The provided city,  does not exist. Therefore, I cannot provide information .
            "It seems like Fake might not be a city, country, or place. Did you mean something else? You can search for information about 'Fake' on the web, or try providing a more specific location."

            Question : What are the travel options available from 'Latur' to 'Fake'  ?
            2 : Fake is not available
            Answer:  The provided city, "fake", does not exist. Therefore, I cannot provide information about traveling from "Latur" to Fake.

            Question: What are the travel options available from 'Solapur' to 'Mumbai' ?
            1: Acknowledging the Request
            I understand you're seeking travel advice from Solapur to Mumbai. Let's explore the available options together.

            2: Verifying Locations
            Both Solapur and Mumbai exist, so we can proceed with planning your trip.

            3: Suggesting Transportation Options
            Direct Options:
            Train: Solapur Junction (SUR) to Mumbai Central (MMCT) via Solapur-Mumbai Express (12140)
            Bus: Solapur Bus Stand to Mumbai Central Bus Stand via MSRTC (Maharashtra State Road Transport Corporation)

            Connecting Options:
            Train via Pune: Solapur Junction (SUR) to Pune Junction (PUNE) via Solapur-Pune Intercity Express (11019), then Pune Junction (PUNE) to Mumbai Central (MMCT) via Deccan Queen Express (12123)
            Bus via Hyderabad: Solapur Bus Stand to Hyderabad Bus Stand via MSRTC, then Hyderabad Bus Stand to Mumbai Central Bus Stand via RedBus

            4: Nearest Place and Connecting Travel Options
            There is no direct path from Solapur to Mumbai by car. The nearest place with a direct connection to Mumbai is Pune.

            Car to Pune: Solapur to Pune via NH65 (approximately 240 km)
            Train from Pune to Mumbai: Pune Junction (PUNE) to Mumbai Central (MMCT) via Deccan Queen Express (12123)

            Recommendation:
            Based on convenience and availability, I recommend taking the direct train from Solapur Junction (SUR) to Mumbai Central (MMCT). It offers a comfortable and efficient journey.


            Question: What are the travel options available from 'Jalgaon' to 'London' ?
            ans: 1: Acknowledging the Request I understand you're seeking travel advice from Jalgaon to London.

            Let's explore the available options together.

            2: Verifying Locations
            Both Jalgaon and London exist, so we can proceed with planning your trip.

            3: Suggesting Transportation Options
            Direct Options:
            There are no direct flights available from Jalgaon to London.

            4: Nearest Place and Connecting Travel Options
            There is no direct path from Jalgaon to London by car. The nearest place with a direct connection to London is Mumbai.

            Car to Mumbai: Jalgaon to Mumbai via NH6 (approximately 400 km)
            Flight from Mumbai to London: Chhatrapati Shivaji Maharaj International Airport (BOM) to Heathrow Airport (LHR) via Air India or British Airways

            Recommendation:
            Based on convenience and availability, I recommend taking the connecting flight option via Mumbai. It offers a wider range of flight schedules and airlines to choose from.


            question: What are the travel options available from 'Naldurg' to 'Solapur' ?
            ans: 1: Acknowledging the Request I understand you're seeking travel advice from Naldurg to Solapur.

            Let's explore the available options together.

            2: Verifying Locations
            Both Naldurg and Solapur exist, so we can proceed with planning your trip.

            3: Suggesting Transportation Options
            Direct Options:
            There are no direct flights available from Naldurg to Solapur.

            4: Nearest Place and Connecting Travel Options
            There is direct path from Naldurg to Solapur by car or bus.

            option1:
            Car to Solapur: Naldurg to Solapur via NH65 (approximately 60 km)
            option2:
            Bus to Solapur: Naldurg Bus Stand to Solapur Bus Stand via NH65

            Recommendation:
            Based on convenience and availability, I recommend taking the bus It offers a comfort and cost efficient.



            Question : What are the travel options available from {origin} to {destination} based on {selected_preference} ?
            Answer:
            """

        return prompt
