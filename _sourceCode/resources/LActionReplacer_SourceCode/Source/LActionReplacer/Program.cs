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
            {"generic_0", "  m_Motion: {fileID: 7400000, guid: 68d5d8ecbb4eccc46a844338727c6518, type: 2}"},
            {"generic_90", "  m_Motion: {fileID: 7400000, guid: 58e073289f7ff5d43a568bd3441a5f11, type: 2}"},
            {"generic_180", "  m_Motion: {fileID: 7400000, guid: 974745045345a5847b9f35856fdf5445, type: 2}"},
            {"generic_270", "  m_Motion: {fileID: 7400000, guid: 972b5ed9d0fd2f14f97f28311ac8552f, type: 2}"},
            {"Fallback", "  m_Motion: {fileID: 7400000, guid: 95b4f16420448c24c84f3faeb8db5364, type: 2}"},
            {"Trunk Close", "  m_Motion: {fileID: 7400000, guid: 4ea070f7501800c47908b156b3744706, type: 2}"},
            {"Trunk Open", "  m_Motion: {fileID: 7400000, guid: 167febd8e9c8c264782fbead770c2bd4, type: 2}"},
            {"Take Loot", "  m_Motion: {fileID: 7400000, guid: 78a4c6195bf01fd42b11d797e62bab49, type: 2}"},
            {"hand_nv_on", "  m_Motion: {fileID: 7400000, guid: aa2b6e112e2f9a54e8f27f89b52c4717, type: 2}"},
            {"hand_nv_off", "  m_Motion: {fileID: 7400000, guid: 06d75af667f280a458e2beb7ad49d5f3, type: 2}"},
            {"hand_key_use", "  m_Motion: {fileID: 7400000, guid: 1fc4a2de1cfdc7b4eb411330ef4e2134, type: 2}"},
            {"hand_drop_stuff", "  m_Motion: {fileID: 7400000, guid: faa4fb1b4e3230148bae486927b08c6e, type: 2}"},
            {"hand_faceshield_off", "  m_Motion: {fileID: 7400000, guid: 7f7abea0c59745b4dbe8ebab42e724fa, type: 2}"},
            {"hand_faceshield_on", "  m_Motion: {fileID: 7400000, guid: 6a85bee344995ab4793613313eefa6ba, type: 2}"},
            {"hand_slap_forward", "  m_Motion: {fileID: 7400000, guid: c0790b5ae61b55f42898c7fad0dcc52e, type: 2}"},
            {"OPEN_PUSH_RIGHT_HINGE", "  m_Motion: {fileID: 7400000, guid: 6791d4566465bdf4fac6ecc91402f5f5, type: 2}"},
            {"OPEN_PUSH_LEFT_HINGE", "  m_Motion: {fileID: 7400000, guid: cbf78601dc4046542b765fdef6fed5af, type: 2}"},
            {"OPEN_PULL_LEFT_HINGE", "  m_Motion: {fileID: 7400000, guid: b7396aa65b0311c48b8c20e3397763a1, type: 2}"},
            {"OPEN_PULL_RIGHT_HINGE", "  m_Motion: {fileID: 7400000, guid: 6791d4566465bdf4fac6ecc91402f5f5, type: 2}"},
            {"pull_hinge_right", "  m_Motion: {fileID: 7400000, guid: 6528fb3df8aa394468d0784e79595fcd, type: 2}"},
            {"pull_hinge_left", "  m_Motion: {fileID: 7400000, guid: 0333fca5280619748abe5ac3e9202b1b, type: 2}"},
            {"push_hinge_left", "  m_Motion: {fileID: 7400000, guid: 68d5d8ecbb4eccc46a844338727c6518, type: 2}"},
            {"push_hinge_right", "  m_Motion: {fileID: 7400000, guid: 4afc9e2e5753b0a4e9da1c0f0dd1541f, type: 2}"}
            //{"compass_out_to_idle", ""},
            //{"compass_idle_to_out", ""},
            //{"compass_use", ""},
        };
        
        private static readonly Dictionary<string, string> GesturesLookup = new()
        {
            {"gestures_00", "    m_Motion: {fileID: 7400000, guid: d39be304f636eb0458e880181728ef4c, type: 2}"},
            {"gestures_01", "    m_Motion: {fileID: 7400000, guid: a71acf374b5959640866648f56eeb551, type: 2}"},
            {"gestures_02", "    m_Motion: {fileID: 7400000, guid: e60809b02c798e94ebb3282d6c33a25d, type: 2}"},
            {"gestures_03", "    m_Motion: {fileID: 7400000, guid: 47e34ce50f3c23043a102399712ef27c, type: 2}"},
            {"gestures_04", "    m_Motion: {fileID: 7400000, guid: 04c76bed1c91fd642b98b490604f1693, type: 2}"},
            {"gestures_05", "    m_Motion: {fileID: 7400000, guid: ebcd78134e634f949bdc09e5b0ad8371, type: 2}"},
            {"gestures_06", "    m_Motion: {fileID: 7400000, guid: b1121030481568845bbf0d4692d7208a, type: 2}"},
        };

        public static void Main(string[] args)
        {
            var lines = ReadControllerLines(out var path);
            int counter = 0;
            
            ReplaceGesturesReference(lines, out var successes);
            counter += successes;
            
            foreach (var name in LActionsLookup.Keys)
            {
                var index = Array.FindIndex(lines, x => x.Contains($"m_Name: {name}"));
                var motionIndex = Array.FindIndex(lines, index, x => x.Contains("m_Motion"));

                if (index == -1 || motionIndex == -1)
                {
                    Console.WriteLine($"{name} is not found in the controller, proceeding to the next LAction");
                    continue;
                }

                Console.WriteLine($"Found {name} in the controller, replacing");
                lines[motionIndex] = LActionsLookup[name];
                counter++;
            }
            
            File.WriteAllLines(path, lines);
            Console.WriteLine($"Replaced a total of {counter} LActions, press any key to exit...");
            Console.ReadKey();
        }

        private static void ReplaceGesturesReference(string[] lines, out int successes)
        {
            successes = 0;
            var index = Array.FindIndex(lines, x => x.Contains("m_BlendParameter: GestureIndex"))-63;
            
            if (index < 0)
            {
                Console.WriteLine($"Gesture blend tree is not found in the controller, aborting gestures replacing");
                return;
            }

            for (int i = 8; i <= 56; i+= 8)
            {
                lines[index+i] = GesturesLookup[$"gestures_0{successes}"];
                successes++;
            }
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