using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace Goofy
{
    internal class Program
    {
        private static readonly Dictionary<string, string> LActionsLookup = new()
        {
            {"weapon_root_anim_fix", "  m_Motion: {fileID: 7400000, guid: f5d6de42a6ad38a47819d80fed8ef704, type: 2}"},
            {"generic_0", "  m_Motion: {fileID: 7400000, guid: 7e68e116281e8764ca5442972e63bd42, type: 2}"},
            {"generic_90", "  m_Motion: {fileID: 7400000, guid: 02216f1a966d5214e98357677fac1a4d, type: 2}"},
            {"generic_180", "  m_Motion: {fileID: 7400000, guid: e8122ffeac79eae4e8b2da92e67ab6e2, type: 2}"},
            {"generic_270", "  m_Motion: {fileID: 7400000, guid: 411676f0ab5383d4cad22e3d37ab03e8, type: 2}"},
            {"Fallback", "  m_Motion: {fileID: 7400000, guid: d1eee6a189a5c0d49861eb7c46fbb47b, type: 2}"},
            {"Trunk Close", "  m_Motion: {fileID: 7400000, guid: 3b8a87d17bb4533418c20f4290ea8508, type: 2}"},
            {"Trunk Open", "  m_Motion: {fileID: 7400000, guid: f9fc3e23472e5b24aa789ace2b24dcc3, type: 2}"},
            {"Take Loot", "  m_Motion: {fileID: 7400000, guid: db026a82f1234694e8d4ae7d25c60f81, type: 2}"},
            {"hand_nv_on", "  m_Motion: {fileID: 7400000, guid: e0198e182a712fc439a8e9cc6a981d4b, type: 2}"},
            {"hand_nv_off", "  m_Motion: {fileID: 7400000, guid: 4f5753f8efdd466449693b6d627e50e2, type: 2}"},
            {"hand_key_use", "  m_Motion: {fileID: 7400000, guid: 01577f7ffe97b8e4d91e80551ee5ad43, type: 2}"},
            {"hand_drop_stuff", "  m_Motion: {fileID: 7400000, guid: f0f710241332e1b44b92558c8854f719, type: 2}"},
            {"hand_faceshield_off", "  m_Motion: {fileID: 7400000, guid: d69ffc0685dd6d541aceb05e5cd4011a, type: 2}"},
            {"hand_faceshield_on", "  m_Motion: {fileID: 7400000, guid: 618103670aaf3104793ce018fd3a1490, type: 2}"},
            {"hand_slap_forward", "  m_Motion: {fileID: 7400000, guid: 43978e2c579084f41bf013a54aa82ddd, type: 2}"},
            {"OPEN_PUSH_RIGHT_HINGE", "  m_Motion: {fileID: 7400000, guid: 24b70f869b5848f449ef39869e2cbebf, type: 2}"},
            {"OPEN_PUSH_LEFT_HINGE", "  m_Motion: {fileID: 7400000, guid: 7051a33c3f945bf428b9471bdfd3e4e7, type: 2}"},
            {"OPEN_PULL_LEFT_HINGE", "  m_Motion: {fileID: 7400000, guid: 1d656d1ad3485cf438fa13ea7a522e7a, type: 2}"},
            {"OPEN_PULL_RIGHT_HINGE", "  m_Motion: {fileID: 7400000, guid: d80524d7cbfa13f4ca51650602391b53, type: 2}"},
            {"pull_hinge_right", "  m_Motion: {fileID: 7400000, guid: dbe2fc508c9a8504294bdfaea90d52a3, type: 2}"},
            {"pull_hinge_left", "  m_Motion: {fileID: 7400000, guid: c7ef54c05e7b7d543ba739accac44f7a, type: 2}"},
            {"push_hinge_left", "  m_Motion: {fileID: 7400000, guid: cbf7362623d7d8e43a71221e11889ac8, type: 2}"},
            {"push_hinge_right", "  m_Motion: {fileID: 7400000, guid: ef5988755f209484ba55722747d6af0d, type: 2}"}
            //{"compass_out_to_idle", ""},
            //{"compass_idle_to_out", ""},
            //{"compass_use", ""},
        };
        
        private static readonly Dictionary<string, string> GesturesLookup = new()
        {
            {"gestures_00", "    m_Motion: {fileID: 7400000, guid: d0d12327826bf10429efc885adce9c4c, type: 2}"},
            {"gestures_01", "    m_Motion: {fileID: 7400000, guid: c92d4a7beeb16c94db4ed396a4b39acc, type: 2}"},
            {"gestures_02", "    m_Motion: {fileID: 7400000, guid: 52c6b5112f031e447b750bee7c88e5c6, type: 2}"},
            {"gestures_03", "    m_Motion: {fileID: 7400000, guid: 11030c3da37700c469f405297f37f50a, type: 2}"},
            {"gestures_04", "    m_Motion: {fileID: 7400000, guid: ecc9009c8edfb114b9d0224e1ab3880f, type: 2}"},
            {"gestures_05", "    m_Motion: {fileID: 7400000, guid: 43c31682dafa38944adfb44971b88c1d, type: 2}"},
            {"gestures_06", "    m_Motion: {fileID: 7400000, guid: 63b5783ae856193428325e536ae75601, type: 2}"},
        };

        public static void Main(string[] args)
        {
            var lines = ReadControllerLines(out var path);
            int counter = 0;
            
            ReplaceGesturesReference(lines, out var successes);
            counter += successes;
            
            foreach (var name in LActionsLookup.Keys)
            {
                // Find the state by name
                var stateIndex = Array.FindIndex(lines, x => x.Contains($"m_Name: {name}"));
                if (stateIndex == -1)
                {
                    Console.WriteLine($"{name} is not found in the controller, proceeding to the next LAction");
                    continue;
                }

                // Search forward from that state for its m_Motion line, but with a bounded window
                // (Unity state blocks are small; 50 lines is plenty and avoids weird cross‑block matches)
                int searchStart = stateIndex;
                int searchCount = Math.Min(50, lines.Length - searchStart);
                int motionIndex = Array.FindIndex(lines, searchStart, searchCount, x => x.Contains("m_Motion"));

                if (motionIndex == -1)
                {
                    Console.WriteLine($"{name} found, but m_Motion line not found nearby, skipping.");
                    continue;
                }

                Console.WriteLine($"Found {name} in the controller, replacing");
                lines[motionIndex] = LActionsLookup[name];
                counter++;
            }

            
            File.WriteAllLines(path, lines);
            Console.WriteLine($"Replaced a total of {counter} LActions.");
        }

    private static void ReplaceGesturesReference(string[] lines, out int successes)
    {
        successes = 0;

        // 1. Find the BlendTree block that uses GestureIndex
        var blendParamIndex = Array.FindIndex(lines, x => x.Contains("m_BlendParameter: GestureIndex"));
        if (blendParamIndex < 0)
        {
            Console.WriteLine("GestureIndex blend tree not found, skipping gestures.");
            return;
        }

        // 2. Walk upwards to find the start of this BlendTree block ("--- !u!206")
        int blockStart = blendParamIndex;
        while (blockStart >= 0 && !lines[blockStart].StartsWith("--- !u!206 "))
            blockStart--;

        if (blockStart < 0)
        {
            Console.WriteLine("Could not locate BlendTree header for GestureIndex, skipping.");
            return;
        }

        // 3. From the block start, find the m_Childs section
        int childLineStart = -1;
        for (int i = blockStart; i < lines.Length; i++)
        {
            if (lines[i].Trim().StartsWith("m_Childs:"))
            {
                childLineStart = i + 1; // first child is on the next line
                break;
            }

            // Safety: stop once we reach another Unity object header
            if (i > blockStart && lines[i].StartsWith("--- !u!"))
                break;
        }

        if (childLineStart < 0)
        {
            Console.WriteLine("m_Childs section not found in GestureIndex BlendTree, skipping.");
            return;
        }

        // 4. Now iterate over children and replace their m_Motion lines
        int gestureIndex = 0;
        for (int i = childLineStart; i < lines.Length && gestureIndex < 7; i++)
        {
            // Stop if we leave the child list (hit a new top‑level field or object)
            if (lines[i].StartsWith("  m_BlendParameter:") || lines[i].StartsWith("--- !u!"))
                break;

            if (lines[i].Trim().StartsWith("m_Motion:"))
            {
                string key = $"gestures_0{gestureIndex}";
                if (GesturesLookup.TryGetValue(key, out var replacement))
                {
                    // Keep indentation from the original line
                    string indent = new string(lines[i].TakeWhile(Char.IsWhiteSpace).ToArray());
                    lines[i] = indent + replacement.Trim();
                    gestureIndex++;
                    successes++;
                }
            }
        }

        Console.WriteLine($"Replaced {successes} gesture motions in GestureIndex blend tree.");
    }


        private static string[] ReadControllerLines(out string path)
        {
            path = Directory.GetFiles(Directory.GetCurrentDirectory()).FirstOrDefault(x => x.EndsWith(".controller"));
            
            if (string.IsNullOrEmpty(path))
            {
                Console.WriteLine(
                    "Drag and drop here animator controller in which you want to fix the LAction animation references.");
                path = Console.ReadLine();
            }

            while (string.IsNullOrEmpty(path) || !path.Contains(".controller"))
            {
                Console.WriteLine("That's not a valid animator controller, it should have .controller extension");
                path = Console.ReadLine();
            }

            var lines = File.ReadAllLines(path);
            return lines;
        }
    }
}