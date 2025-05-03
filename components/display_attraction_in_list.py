
def display_ride_as_item_in_list(_, st, attraction):
    with st.container(border=True):
        col1, col2 = st.columns([.7, .3])
        with col1:
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:15px; margin-bottom:10px;">
                    <h2 style="margin:0; font-size:24px; color:#FF8B17;">{attraction.name}</h2>
                </div>
                <div style="display:flex; align-items:center; padding:15px; box-shadow:2px 2px 10px rgba(0,0,0,0.1); margin-bottom:20px;">
                    <div style="flex:2; padding-right:15px;">
                        <p style="font-size:14px; color:#555; margin:5px 0; display:flex; align-items:center; gap:5px;">
                            <span style="background-color:#3399ff; color:white; padding:3px 8px; border-radius:5px; font-weight:bold;">
                                {attraction.attraction_type}
                            </span>
                            <span style="background-color:#ff5733; color:white; padding:3px 8px; border-radius:5px; font-weight:bold;">
                                {attraction.manufacturer}
                            </span>
                            <span style="background-color:#33cc33; color:white; padding:3px 8px; border-radius:5px; font-weight:bold;">
                                {attraction.technical_name or "_"}
                            </span>
                            <span style="flex-grow:1;"></span>
                            <span style="background-color:#ffcc00; color:black; padding:3px 8px; border-radius:5px; font-weight:bold;">
                                {attraction.ticket_price:.2f} €
                            </span>
                        </p>
                        <p style="margin-top:10px;">{attraction.description}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col2:
            if st.button(_("View ride details"), key=f"view_ride_{attraction.id}_detail", use_container_width=True):
                st.session_state.ride_id = attraction.id
                st.switch_page("pages/ride_view.py")

            if len(attraction.images):
                image = attraction.images[0]
                st.image(image.path, use_container_width=True)
