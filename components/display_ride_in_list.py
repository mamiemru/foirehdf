from components.image_loader import fetch_cached_image


def display_ride_as_item_in_list(_, st, ride) -> None:
    """
    Display a ride in a box.
    
    Args:
        _ (translation): translation function.
        st (streamlit): streamlit instance.
        ride: a Ride object.

    """
    with st.container(border=True):
        col1, col2 = st.columns([.7, .3])
        with col1:
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:15px; margin-bottom:10px;">
                    <h2 style="margin:0; font-size:24px; color:#FF8B17;">{ride.name}</h2>
                </div>
                <div style="display:flex; align-items:center; padding:15px; margin-bottom:20px;">
                    <div style="flex:2; padding-right:15px;">
                        <p style="font-size:14px; color:#555; margin:5px 0; display:flex; align-items:center; gap:5px;">
                            <span style="background-color:#3399ff; color:white; padding:3px 8px; border-radius:5px; font-weight:bold;">
                                {ride.ride_type}
                            </span>
                            <span style="background-color:#ff5733; color:white; padding:3px 8px; border-radius:5px; font-weight:bold;">
                                {ride.manufacturer}
                            </span>
                            <span style="background-color:#33cc33; color:white; padding:3px 8px; border-radius:5px; font-weight:bold;">
                                {ride.technical_name or "_"}
                            </span>
                            <span style="flex-grow:1;"></span>
                            <span style="background-color:#ffcc00; color:black; padding:3px 8px; border-radius:5px; font-weight:bold;">
                                {ride.ticket_price:.2f} €
                            </span>
                        </p>
                        <p style="margin-top:10px;">{ride.description or ''}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col2:
            if st.button(_("VIEW_RIDE_DETAILS"), key=f"view_ride_{ride.id}_detail", use_container_width=True):
                st.session_state.ride_id = ride.id
                st.switch_page("pages/ride_view.py")

            if len(ride.images_url):
                image = fetch_cached_image(ride.images_url[0])
                if image:
                    st.image(image, use_container_width=True)
