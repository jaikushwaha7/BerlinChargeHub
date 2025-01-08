from graphviz import Digraph

def create_domain_event_flow_diagrams():
    # Diagram for "Search Charging Stations by Postal Code"
    search_flow = Digraph("SearchDomainEventFlow", format="png")
    search_flow.attr(rankdir="LR")  # Left to Right layout
    search_flow.node("User", "User", shape="ellipse")
    search_flow.node("StationSearchPerformed", "Station Search Performed", shape="box")
    search_flow.node("ValidatePostalCode", "Validate Postal Code", shape="parallelogram")
    search_flow.node("ChargingStationRepository", "Charging Station Repository", shape="cylinder")
    search_flow.node("SearchResult", "Search Result", shape="box")

    search_flow.edges([
        ("User", "StationSearchPerformed"),
        ("StationSearchPerformed", "ValidatePostalCode"),
        ("ValidatePostalCode", "ChargingStationRepository"),
        ("ChargingStationRepository", "SearchResult"),
        ("SearchResult", "User")
    ])
    search_flow.render("Search_Charging_Stations_Event_Flow", cleanup=True)

    # Diagram for "Rate Charging Stations"
    rate_flow = Digraph("RateChargingStationsEventFlow", format="png")
    rate_flow.attr(rankdir="LR")  # Left to Right layout
    rate_flow.node("User", "User", shape="ellipse")
    rate_flow.node("StationFeedbackSubmitted", "Station Feedback Submitted", shape="box")
    rate_flow.node("FeedbackRepository", "Feedback Repository", shape="cylinder")
    rate_flow.node("FeedbackAggregated", "Feedback Aggregated", shape="box")
    rate_flow.node("FeedbackAggregationService", "Feedback Aggregation Service", shape="parallelogram")
    rate_flow.node("ChargingStationRepository", "Charging Station Repository", shape="cylinder")

    rate_flow.edges([
        ("User", "StationFeedbackSubmitted"),
        ("StationFeedbackSubmitted", "FeedbackRepository"),
        ("StationFeedbackSubmitted", "FeedbackAggregationService"),
        ("FeedbackAggregationService", "FeedbackRepository"),
        ("FeedbackRepository", "FeedbackAggregated"),
        ("FeedbackAggregated", "ChargingStationRepository"),
        ("FeedbackAggregated", "User")
    ])
    rate_flow.render("Rate_Charging_Stations_Event_Flow", cleanup=True)

def create_component_interaction_sequence_diagrams():
    # Diagram for "Search Charging Stations by Postal Code"
    search_sequence = Digraph("SearchSequenceDiagram", format="png")
    search_sequence.attr(rankdir="TB")  # Top to Bottom layout
    search_sequence.node("User", "User", shape="ellipse")
    search_sequence.node("SearchService", "Search Service", shape="box")
    search_sequence.node("ChargingStationService", "Charging Station Service", shape="box")
    search_sequence.node("ChargingStationRepository", "Charging Station Repository", shape="cylinder")

    search_sequence.edges([
        ("User", "SearchService"),
        ("SearchService", "ChargingStationService"),
        ("ChargingStationService", "ChargingStationRepository"),
        ("ChargingStationRepository", "ChargingStationService"),
        ("ChargingStationService", "SearchService"),
        ("SearchService", "User")
    ])
    search_sequence.render("Search_Charging_Stations_Sequence_Diagram", cleanup=True)

    # Diagram for "Rate Charging Stations"
    rate_sequence = Digraph("RateSequenceDiagram", format="png")
    rate_sequence.attr(rankdir="TB")  # Top to Bottom layout
    rate_sequence.node("User", "User", shape="ellipse")
    rate_sequence.node("RatingService", "Rating Service", shape="box")
    rate_sequence.node("FeedbackRepository", "Feedback Repository", shape="cylinder")
    rate_sequence.node("FeedbackAggregationService", "Feedback Aggregation Service", shape="box")
    rate_sequence.node("ChargingStationRepository", "Charging Station Repository", shape="cylinder")

    rate_sequence.edges([
        ("User", "RatingService"),
        ("RatingService", "FeedbackRepository"),
        ("RatingService", "FeedbackAggregationService"),
        ("FeedbackAggregationService", "FeedbackRepository"),
        ("FeedbackAggregationService", "ChargingStationRepository"),
        ("ChargingStationRepository", "FeedbackAggregationService"),
        ("FeedbackAggregationService", "RatingService"),
        ("RatingService", "User")
    ])
    rate_sequence.render("Rate_Charging_Stations_Sequence_Diagram", cleanup=True)

if __name__ == "__main__":
    create_domain_event_flow_diagrams()
    create_component_interaction_sequence_diagrams()
