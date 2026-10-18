package in.rrbpractice.lite;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.util.AtomicFile;
import android.view.View;
import android.webkit.JavascriptInterface;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import org.json.JSONObject;

/** Platform-only offline shell. No Internet or storage permissions. */
public final class MainActivity extends Activity {
    private WebView web;
    private AtomicFile state;
    private static final int IMPORT=21, EXPORT=22;
    private String pendingExport;
    private static final Set<String> ASSETS=new HashSet<>(Arrays.asList("index.html","style.css","core.js","app.js","bank.json","storage.js","backup.js","platform.js","manifest.webmanifest","icon-192.png","icon-512.png"));
    @Override public void onCreate(Bundle saved) {
        super.onCreate(saved);
        state=new AtomicFile(new File(getFilesDir(),"practice-state.json"));
        web=new WebView(this);
        web.setBackgroundColor(Color.rgb(245,247,244));
        // Account for system bars, including Android 15's edge-to-edge enforcement.
        web.setOnApplyWindowInsetsListener((view,insets)->{
            view.setPadding(insets.getSystemWindowInsetLeft(),insets.getSystemWindowInsetTop(),insets.getSystemWindowInsetRight(),insets.getSystemWindowInsetBottom());
            return insets.consumeSystemWindowInsets();
        });
        setContentView(web);
        getWindow().setStatusBarColor(Color.rgb(20,47,56));
        getWindow().setNavigationBarColor(Color.WHITE);
        if(android.os.Build.VERSION.SDK_INT>=26)web.setSystemUiVisibility(View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR);
        WebSettings settings=web.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        settings.setSupportMultipleWindows(false);
        settings.setJavaScriptCanOpenWindowsAutomatically(false);
        web.addJavascriptInterface(new Bridge(),"Android");
        web.setWebViewClient(new WebViewClient(){
            @Override public WebResourceResponse shouldInterceptRequest(WebView view,WebResourceRequest request){
                Uri uri=request.getUrl();String path=uri.getPath();
                if("https".equals(uri.getScheme())&&"app.local".equals(uri.getHost())&&path!=null){
                    String name=path.equals("/")?"index.html":path.substring(1);
                    if(ASSETS.contains(name))try{
                        String mime=name.endsWith(".js")?"application/javascript":name.endsWith(".css")?"text/css":name.endsWith(".json")?"application/json":name.endsWith(".webmanifest")?"application/manifest+json":name.endsWith(".png")?"image/png":"text/html";
                        return new WebResourceResponse(mime,"UTF-8",getAssets().open(name));
                    }catch(IOException ignored){}
                }
                return new WebResourceResponse("text/plain","UTF-8",403,"Blocked",Collections.emptyMap(),new ByteArrayInputStream(new byte[0]));
            }
            @Override public boolean shouldOverrideUrlLoading(WebView view,WebResourceRequest request){
                Uri uri=request.getUrl();
                if("https".equals(uri.getScheme())&&"app.local".equals(uri.getHost()))return false;
                if(request.isForMainFrame()&&"https".equals(uri.getScheme()))try{startActivity(new Intent(Intent.ACTION_VIEW,uri));}catch(Exception e){error("No browser is available for that link.");}
                return true;
            }
        });
        web.loadUrl("https://app.local/index.html");
    }
    private static String readLimited(InputStream in,int max)throws IOException {
        try(InputStream src=in;ByteArrayOutputStream out=new ByteArrayOutputStream()){
            byte[] buffer=new byte[8192];int n;
            while((n=src.read(buffer))!=-1){if(out.size()+n>max)throw new IOException("File is too large");out.write(buffer,0,n);}
            return out.toString("UTF-8");
        }
    }
    public final class Bridge {
        @JavascriptInterface public String readState(){
            synchronized(MainActivity.this){try{return readLimited(state.openRead(),24*1024*1024);}catch(FileNotFoundException e){return "";}catch(Exception e){return "INVALID_SAVED_STATE";}}
        }
        @JavascriptInterface public String writeState(String value){
            if(value==null||value.length()>24*1024*1024)return "State exceeds storage limit";
            synchronized(MainActivity.this){FileOutputStream out=null;try{out=state.startWrite();out.write(value.getBytes(StandardCharsets.UTF_8));state.finishWrite(out);return "";}catch(Exception e){if(out!=null)state.failWrite(out);return "Could not save state";}}
        }
        @JavascriptInterface public void importPack(){runOnUiThread(()->{try{Intent intent=new Intent(Intent.ACTION_OPEN_DOCUMENT);intent.addCategory(Intent.CATEGORY_OPENABLE);intent.setType("*/*");intent.putExtra(Intent.EXTRA_MIME_TYPES,new String[]{"application/json","text/plain","application/octet-stream"});startActivityForResult(intent,IMPORT);}catch(Exception e){error("The file picker is unavailable.");}});}
        @JavascriptInterface public void exportPack(String name,String value){runOnUiThread(()->{try{if(value==null||value.length()>24*1024*1024)throw new IOException();pendingExport=value;Intent intent=new Intent(Intent.ACTION_CREATE_DOCUMENT);intent.addCategory(Intent.CATEGORY_OPENABLE);intent.setType("application/json");intent.putExtra(Intent.EXTRA_TITLE,name);startActivityForResult(intent,EXPORT);}catch(Exception e){pendingExport=null;error("Could not open the save picker.");}});}
    }
    private void error(String message){runOnUiThread(()->web.evaluateJavascript("window.nativeError("+JSONObject.quote(message)+");",null));}
    @Override protected void onActivityResult(int request,int result,Intent data){
        super.onActivityResult(request,result,data);
        if(result!=RESULT_OK||data==null||data.getData()==null){if(request==EXPORT)pendingExport=null;return;}
        Uri uri=data.getData();
        if(request==IMPORT){new Thread(()->{try{String text=readLimited(getContentResolver().openInputStream(uri),24*1024*1024);runOnUiThread(()->web.evaluateJavascript("window.receiveImport("+JSONObject.quote(text)+");",null));}catch(Exception e){error("Could not read pack. Choose a JSON file smaller than 24 MB.");}},"pack-import").start();}
        if(request==EXPORT){final String value=pendingExport;pendingExport=null;if(value==null){error("Save was interrupted. Please export again.");return;}new Thread(()->{try(OutputStream out=getContentResolver().openOutputStream(uri,"wt")){if(out==null)throw new IOException();out.write(value.getBytes(StandardCharsets.UTF_8));error("Question pack saved.");}catch(Exception e){error("Could not save that file. Please export again.");}},"pack-export").start();}
    }
    @Override public void onBackPressed(){web.evaluateJavascript("window.onNativeBack ? window.onNativeBack() : false",value->{if(!"true".equals(value))finish();});}
    @Override protected void onDestroy(){if(web!=null){web.removeJavascriptInterface("Android");web.destroy();}super.onDestroy();}
}
