require 'test_helper'

class DictionaryControllerTest < ActionDispatch::IntegrationTest
  test "should get dictionary" do
    get dictionary_dictionary_url
    assert_response :success
  end

end
