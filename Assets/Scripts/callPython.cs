using UnityEngine;
using UnityEditor;
using UnityEditor.Callbacks;
using System.IO;
using System.Diagnostics;
using System.Collections;

public class PostProcessBuildProcessor {

    [PostProcessBuild]
    public static void OnPostProcessBuild(BuildTarget target, string path) {
        var output = DoBashCommand("echo hello");
        UnityEngine.Debug.Log(output);
    }

    static string DoBashCommand(string cmd){
        var p = new Process();
        p.StartInfo.FileName = "/bin/bash";
        p.StartInfo.Arguments = "-c \" " + cmd + " \"";
        p.StartInfo.UseShellExecute = false;
        p.StartInfo.RedirectStandardOutput = true;
        p.Start();

        var output = p.StandardOutput.ReadToEnd();
        p.WaitForExit();
        p.Close();

        return output;
    }
}