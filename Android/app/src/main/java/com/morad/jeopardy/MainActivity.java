package com.morad.jeopardy;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.WindowManager;
import android.webkit.ConsoleMessage;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.webkit.WebViewAssetLoader;
import androidx.webkit.WebViewClientCompat;

/**
 * The show exists once, as the web build, and every app is a window onto it.
 * Nothing below decides how anything looks or sounds — it finds the build in the
 * assets, hands it to a webview, and gets out of the way.
 *
 * This is the Android reading of `App/ShowWebView.swift`, and it keeps the same
 * two promises that file makes: the game plays itself without waiting to be
 * tapped, and the window is a stage rather than a document.
 */
public class MainActivity extends Activity {

    /** Where the staged tree lives, and therefore the origin the page runs from. */
    private static final String SHOW_URL =
            "https://appassets.androidplatform.net/assets/Web/index.html";
    private static final String TAG = "Jeopardy";

    private WebView show;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);

        // A game show runs for an hour without anybody touching the screen.
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        goFullScreen();

        show = new WebView(this);
        dressStage(show);
        arrange(show);

        setContentView(show);
        show.loadUrl(SHOW_URL);
    }

    /**
     * A game show is not a web page. The theme and the host's line start on their
     * own, so the webview must not sit on them waiting for a tap that the app
     * never asks anybody for — the same reason the Swift shell clears
     * `mediaTypesRequiringUserActionForPlayback`.
     */
    private void arrange(WebView view) {
        WebSettings settings = view.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setMediaPlaybackRequiresUserGesture(false);

        // The page is served by the loader below, so it has no business reaching
        // the filesystem — not its own, and not the device's.
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);

        // A fixed 1672x941 canvas, laid out by the stylesheet and sized to the
        // window. The viewport is the stage; nothing about it is a document to
        // be panned around.
        settings.setUseWideViewPort(false);
        settings.setLoadWithOverviewMode(false);
        settings.setSupportZoom(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);
        settings.setTextZoom(100);
    }

    /** A stage, not a document: no bouncing, no zooming, no long-press menu. */
    private void dressStage(WebView view) {
        view.setBackgroundColor(Color.BLACK);
        view.setOverScrollMode(View.OVER_SCROLL_NEVER);
        view.setVerticalScrollBarEnabled(false);
        view.setHorizontalScrollBarEnabled(false);
        view.setLongClickable(false);
        view.setHapticFeedbackEnabled(false);
        // The controls are chosen with a thumb landing on a plate; a selection
        // handle appearing instead would be the wrong answer to the same gesture.
        view.setOnLongClickListener(v -> true);

        final WebViewAssetLoader loader = new WebViewAssetLoader.Builder()
                .addPathHandler("/assets/", new WebViewAssetLoader.AssetsPathHandler(this))
                .build();

        view.setWebViewClient(new WebViewClientCompat() {
            @Nullable
            @Override
            public WebResourceResponse shouldInterceptRequest(
                    @NonNull WebView webView, @NonNull WebResourceRequest request) {
                return loader.shouldInterceptRequest(request.getUrl());
            }
        });

        // Not for the player: a webview has no console anywhere else, and a silent
        // failure inside the show is the one thing this shell could hide.
        view.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onConsoleMessage(@NonNull ConsoleMessage message) {
                Log.d(TAG, message.message() + " @" + message.lineNumber());
                return true;
            }
        });
    }

    private void goFullScreen() {
        getWindow().setFlags(
                WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            getWindow().setDecorFitsSystemWindows(false);
        }
        showImmersive();
    }

    /** Sticky, so the bars stay gone for as long as the show is running. */
    private void showImmersive() {
        View decor = getWindow().getDecorView();
        decor.setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                        | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                        | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN);
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) showImmersive();
    }

    @Override
    protected void onPause() {
        super.onPause();
        // A show that keeps playing to an empty room. The page holds its own
        // place, so it is only the sound that has to stop.
        if (show != null) {
            show.onPause();
            show.pauseTimers();
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (show != null) {
            show.resumeTimers();
            show.onResume();
        }
    }

    @Override
    protected void onDestroy() {
        if (show != null) {
            show.loadUrl("about:blank");
            show.destroy();
            show = null;
        }
        super.onDestroy();
    }
}
