using System.IO;
using System.Net;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Json;
using System.Web.Script.Serialization;


// Base64形式の汎用操作を提供するクラス
public static class Base64
{
    // 指定した通常の文字列をUTF-8としてBase64文字列に変換する
    public static string Encode(string str)
    {
        return Encode(str, Encoding.UTF8);
    }

    // 指定したBase64文字列をUTF-8として通常の文字列に変換する
    public static string Decode(string base64Str)
    {
        return Decode(base64Str, Encoding.UTF8);
    }
    
    // ファイルの内容を読み取ってそ内容をBase64文字列として取得する
    public static string ReadWithEncode(string filePath)
    {
        return Convert.ToBase64String(File.ReadAllBytes(filePath));
    }

    // Base64文字列を通常の文字列に変換してファイルに保存します
    public static void SaveWithDecode(string base64Str, string savePath)
    {
        byte[] barray = Convert.FromBase64String(base64Str);
        using (var fs = new FileStream(savePath, FileMode.Create))
        {
            fs.Write(barray, 0, barray.Length);
        }
    }
}

class test_post
{
    static void Main(string[] args)
    {
        string filePath = @"./temp.jpg";
        string encodeBody = Base64.ReadWithEncode(filePath);
        HttpWebRequest req = (HttpWebRequest)WebRequest.Create("http://0.0.0.0:5000/");
        req.ContentType = "application/json";
        req.Method = "POST";
        using (var streamWriter = new StreamWriter(req.GetRequestStream()))
        {
            string jsonPayload = new JavaScriptSerializer().Serialize(new
            {
                temp = encodeBody
            });
            streamWriter.Write(jsonPayload);
        }
        HttpWebResponse res = (HttpWebResponse)req.GetResponse();
        RequestResult result;
        using (res)
        {
            using (var resStream = res.GetResponseStream())
            {
                var serializer = new DataContractJsonSerializer(typeof(RequestResult));
                result = (RequestResult)serializer.ReadObject(resStream);
            }
        }
    }
}