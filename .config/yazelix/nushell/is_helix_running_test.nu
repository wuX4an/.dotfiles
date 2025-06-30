#!/usr/bin/env nu

# Run this with `nu ~/.config/yazelix/nushell/is_hx_running_test.nu`

use std assert

# Import the function to test from utils.nu
use ~/.config/yazelix/nushell/utils.nu is_hx_running

# Define test cases
def test_cases [] {
    [
        # Basic cases for 'hx'
        ["hx", true, "Basic 'hx' command"],
        ["HX", true, "Uppercase 'HX'"],
        ["hx ", true, "hx with trailing space"],
        [" hx", true, "hx with leading space"],
        
        # Path cases for 'hx'
        ["/hx", true, "hx at root"],
        ["/usr/local/bin/hx", true, "Full path to hx"],
        ["./hx", true, "Relative path to hx"],
        ["../hx", true, "Parent directory hx"],
        ["some/path/to/hx", true, "Nested path to hx"],
        
        # With arguments for 'hx'
        ["hx .", true, "hx with current directory"],
        ["hx file.txt", true, "hx with file argument"],
        ["hx -c theme:base16", true, "hx with flag"],
        ["hx --help", true, "hx with long flag"],
        ["/usr/local/bin/hx --version", true, "Full path hx with flag"],
        
        # Basic cases for 'helix'
        ["helix", true, "Basic 'helix' command"],
        ["HELIX", true, "Uppercase 'HELIX'"],
        ["helix ", true, "helix with trailing space"],
        [" helix", true, "helix with leading space"],
        
        # Path cases for 'helix'
        ["/helix", true, "helix at root"],
        ["/usr/local/bin/helix", true, "Full path to helix"],
        ["./helix", true, "Relative path to helix"],
        ["../helix", true, "Parent directory helix"],
        ["some/path/to/helix", true, "Nested path to helix"],
        
        # With arguments for 'helix'
        ["helix .", true, "helix with current directory"],
        ["helix file.txt", true, "helix with file argument"],
        ["helix -c theme:base16", true, "helix with flag"],
        ["helix --help", true, "helix with long flag"],
        ["/usr/local/bin/helix --version", true, "Full path helix with flag"],
        
        # Negative cases
        ["vim", false, "Different editor"],
        ["echo hx", false, "hx in echo command"],
        ["echo helix", false, "helix in echo command"],
        ["path/with/hx/in/middle", false, "hx in middle of path"],
        ["path/with/helix/in/middle", false, "helix in middle of path"],
        ["hx_file", false, "hx as part of filename"],
        ["helix_file", false, "helix as part of filename"],
        ["not_helix", false, "helix as part of word"],
    ]
}

# Run tests
def run_tests [] {
    mut passed_count = 0
    let n_tests = (test_cases | length)
    
    for case in (test_cases) {
        let input = $case.0
        let expected = $case.1
        let description = $case.2
        
        print $"Testing: ($description)"
        let result = (is_hx_running $input)
        assert equal $result $expected $"Failed: ($description) - Expected ($expected), got ($result)"
        
        # If the assertion passes, increment the counter and print the number of passed tests
        $passed_count = $passed_count + 1
        print $"Passed test #($passed_count) of ($n_tests): ($description)"
        print ""
    }
    
    print $"Total tests passed: ($passed_count)"
}

# Main test runner
def main [] {
    print "Running tests for is_hx_running function..."
    run_tests
    print "All tests completed!"
}
