import streamlit as st
from planner import plan_trip

# Title of the app
st.title("Travel Planner 📒")

# Input fields for current location and destination
current_location = st.text_input(label="Enter your Current Location", placeholder="Current Location")
destination = st.text_input(label="Enter your Destination", placeholder="Destination")

# Helper function to display travel option details
def display_travel_option(option_data):
    if isinstance(option_data, dict):
        # Display key travel details
        st.markdown(f"**Best Route:** {option_data.get('best_route', 'N/A')}")
        st.markdown(f"**Description:** {option_data.get('description', 'N/A')}")
        st.markdown(f"**Estimated Travel Time:** {option_data.get('estimated_travel_time', 'N/A')}")

        # Handle estimated cost (could be a dictionary or a string)
        cost = option_data.get('estimated_cost', 'N/A')
        if isinstance(cost, dict):
            st.markdown("**Estimated Cost:**")
            for key, value in cost.items():
                st.markdown(f"- {key.capitalize()}: {value}")
        else:
            st.markdown(f"**Estimated Cost:** {cost}")

        # Total Estimated Cost
        st.markdown(f"**Total Estimated Cost:** {option_data.get('total_estimated_cost', 'N/A')}")

        # Display pros if present
        pros = option_data.get('pros', [])
        if pros:
            st.markdown("**Pros:**")
            for pro in pros:
                st.markdown(f"- {pro}")

        # Display cons if present
        cons = option_data.get('cons', [])
        if cons:
            st.markdown("**Cons:**")
            for con in cons:
                st.markdown(f"- {con}")
    else:
        st.info("No travel plan available for this option")

# Button to trigger the travel planning
if st.button(label="Let's Navigate!"):
    if not current_location or not destination:
        st.error("Please enter both Current Location and Destination.")
    else:
        # Get the travel plan from the planner
        travel_plan = plan_trip(current_location, destination)

        # Create three columns for Road, Train, and Air
        col1, col2, col3 = st.columns(3)

        # Road column
        with col1:
            st.markdown("### ROAD 🛣️")
            road_data = travel_plan.get("road", {})
            display_travel_option(road_data)

        # Train column
        with col2:
            st.markdown("### TRAIN 🛤️")
            train_data = travel_plan.get("train", {})
            display_travel_option(train_data)

        # Air column (using "flight" key)
        with col3:
            st.markdown("### AIR ✈️")
            flight_data = travel_plan.get("flight", {})
            display_travel_option(flight_data)

        # Display overall recommendation if available
        recommendation = travel_plan.get("recommendation", "")
        if recommendation:
            st.markdown("### Recommendation")
            st.info(recommendation)