# sc4fuzz
**Text Rendering Stress Tester and Fuzzer**

sc4fuzz is a security research tool written in Python designed to generate complex Unicode text payloads. It is used to fuzz and stress-test text rendering engines (messaging applications, browsers, or terminals) against **Denial of Service (DoS)** vulnerabilities or resource exhaustion caused by recursive, Bidi, and ZWJ sequences.

---

## What does sc4fuzz do?
Modern applications often struggle to handle specific Unicode sequences efficiently. sc4fuzz helps security researchers and QA engineers simulate extreme workloads on text parsers through several techniques:

- **Invisible Bloat (ZWSP)**: Fills memory buffers with invisible Zero-Width Space characters.
- **Bidi Logic Stress**: Forces Bidirectional (RLE/RLM) algorithms into heavy layout recalculations.
- **Deep Recursion**: Tests the depth limits of Markdown/formatting parsers through nested sequences.
- **Zalgo Stack**: Stacks diacritic marks to test vertical rendering boundaries and overflow.
- **Emoji ZWJ Clusters**: Stresses the logic of complex glyph merging (Zero Width Joiners).

---

## Installation

Clone the repository and ensure you have Python 3.x installed:

```bash
git clone https://github.com/sc4redy/sc4fuzz.git
cd sc4fuzz
```

## Usage Guide
Use the `-t` flag to select a payload type and `-o` to save the output.

**Examples:**
1. Generate a Deep Zalgo Bomb:
   ``` bash
   python3 sc4fuzz.py -t zalgo -c 5000 -d 100 -o zalgo_test.txt
   ```
2. Generate a Bidi Logic Stress Test:
   ``` bash
   python3 sc4fuzz.py -t bidi -c 20000 --show
   ```
3. Simulate Deep Markdown Recursion:
   ``` bash
   python3 sc4fuzz.py -t recursive -d 250 -f "*" -o recursive_test.txt
   ```
   **Parameters:**
   ```text
    Flag            Description                                         Default
    -t, --type      Payload type (zwsp, bidi, zalgo, recursive, emoji)  Required
    -c, --count     Number of base characters or repetitions            10000
    -d, --depth     Stack depth or recursion depth (zalgo/recursive)    20
    -o, --output    Filename to save the payload                        fuzz_payload.txt
    --show          Preview the payload in the console                  false
   ```
