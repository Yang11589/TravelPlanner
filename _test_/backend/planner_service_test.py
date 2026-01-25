from app.services.planner_service import generate_plan

def test_generate_plan_basic():
    result = generate_plan("harbin", 3)

    assert result.city == "harbin"
    assert result.days == 3
    assert len(result.itinerary) == 3

    for i, day in enumerate(result.itinerary):
        assert day.day == i + 1
        assert len(day.places) == 2
