package com.example.particle;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;

import androidx.appcompat.app.AppCompatActivity;

public class Splash extends Activity {
    private static int SPLASH_TIME_OUT = 4000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.splash);
        new Handler().postDelayed(new Runnable(){
            @Override
            public void run(){
                startActivity(new Intent(Splash.this, HomeActivity.class));
                finish();
            }
        }, SPLASH_TIME_OUT);
    }
}
