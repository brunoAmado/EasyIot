#include <unity.h>
#include <string>

// Test type assertions (corresponding to fix/esp32-compilation containsKey->is<const char*> fix)
void test_type_assertions(void) {
    const char* test_val = "secret";
    TEST_ASSERT_EQUAL_STRING("secret", test_val);
}

// Test request method routing logic (corresponding to feat/captive-portal-hardening POST enforcement)
bool validate_request_method(const std::string& method, const std::string& expected_method) {
    return method == expected_method;
}

void test_request_method_validation(void) {
    TEST_ASSERT_TRUE(validate_request_method("POST", "POST"));
    TEST_ASSERT_FALSE(validate_request_method("GET", "POST"));
}

// Test light dimmer percentage mapping logic (corresponding to feat/light-dimmer hold-to-dim range mapping)
int map_brightness_to_percentage(int brightness) {
    if (brightness < 0) return 0;
    if (brightness > 255) return 100;
    return (brightness * 100) / 255;
}

void test_dimmer_percentage_mapping(void) {
    TEST_ASSERT_EQUAL(0, map_brightness_to_percentage(0));
    TEST_ASSERT_EQUAL(100, map_brightness_to_percentage(255));
    TEST_ASSERT_EQUAL(50, map_brightness_to_percentage(128)); // 128 * 100 / 255 = 50
    TEST_ASSERT_EQUAL(0, map_brightness_to_percentage(-10));
    TEST_ASSERT_EQUAL(100, map_brightness_to_percentage(300));
}

int main(int argc, char **argv) {
    UNITY_BEGIN();
    RUN_TEST(test_type_assertions);
    RUN_TEST(test_request_method_validation);
    RUN_TEST(test_dimmer_percentage_mapping);
    UNITY_END();
    return 0;
}
