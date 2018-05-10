require 'test_helper'

class HistoryControllerTest < ActionDispatch::IntegrationTest
  test "should get history" do
    get history_history_url
    assert_response :success
  end

end
