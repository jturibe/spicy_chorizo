package com.example.particle;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.cardview.widget.CardView;
import androidx.core.content.ContextCompat;
import androidx.viewpager.widget.ViewPager;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.google.firebase.messaging.FirebaseMessaging;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

import static android.content.ContentValues.TAG;

public class HomeActivity extends Activity {

    ImageButton settingsButton;
    LinearLayout temperaturePanel;
    LinearLayout humidityPanel;
    ViewPager viewPager;
    boolean temp_graphs;
    boolean hum_graphs;
    ViewPagerAdapter viewPagerAdapter;
    LinearLayout sliderDotspanel;
    private int dotscount;
    private ImageView[] dots;

    public void onCreate(Bundle savedInstanceState){
        temp_graphs = true;
        hum_graphs = false;
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);
        FirebaseMessaging.getInstance().subscribeToTopic("event_updates");
        updateStats();
        settingsButton = findViewById(R.id.settingsButton);
        settingsButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(HomeActivity.this, displaySettings.class);
                startActivity(intent);
            }
        });

        sliderDotspanel = (LinearLayout) findViewById(R.id.SliderDots);

        viewPager = (ViewPager) findViewById(R.id.viewPager);
        ArrayList<Bitmap> default_bitmaps = new ArrayList<>();
        Bitmap def = BitmapFactory.decodeResource(getResources(), R.drawable.defaultwhite);
        for(int i = 0; i < 3; i++){
            default_bitmaps.add(def);
        }
        viewPagerAdapter = new ViewPagerAdapter(default_bitmaps, this);
        viewPager.setAdapter(viewPagerAdapter);
        dotscount = viewPagerAdapter.getCount();
        dots = new ImageView[dotscount];

        for (int i = 0; i < dotscount; i++) {

            dots[i] = new ImageView(this);
            dots[i].setImageDrawable(ContextCompat.getDrawable(getApplicationContext(),
                    R.drawable.nonactive_dot));

            LinearLayout.LayoutParams params = new LinearLayout.LayoutParams
                    (LinearLayout.LayoutParams.WRAP_CONTENT,
                            LinearLayout.LayoutParams.WRAP_CONTENT);

            params.setMargins(8,0,8,0);

            sliderDotspanel.addView(dots[i], params);
        }

        dots[0].setImageDrawable(ContextCompat.getDrawable(getApplicationContext(),
                R.drawable.active_dot));

        viewPager.addOnPageChangeListener(new ViewPager.OnPageChangeListener() {
            @Override
            public void onPageScrolled(int position, float positionOffset, int positionOffsetPixels) {

            }

            @Override
            public void onPageSelected(int position) {

                for (int i = 0; i < dotscount; i++) {
                    dots[i].setImageDrawable(ContextCompat.getDrawable(getApplicationContext(),
                            R.drawable.nonactive_dot));
                }

                dots[position].setImageDrawable(ContextCompat.getDrawable(getApplicationContext(),
                        R.drawable.active_dot));

            }

            @Override
            public void onPageScrollStateChanged(int state) {

            }
        });

        temperaturePanel = findViewById(R.id.temp_panel);
        temperaturePanel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                TextView current_temperature_text = findViewById(R.id.current_temperature);
                current_temperature_text.setTextColor(Color.parseColor("#000000"));
                TextView temperature_label_text = findViewById(R.id.temp_label);
                temperature_label_text.setTextColor(Color.parseColor("#000000"));
                TextView current_humidity_text = findViewById(R.id.current_humidity);
                current_humidity_text.setTextColor(Color.parseColor("#707070"));
                TextView humidity_label_text = findViewById(R.id.hum_label);
                humidity_label_text.setTextColor(Color.parseColor("#707070"));
                temp_graphs = true;
                hum_graphs = false;
                FirebaseDatabase database = FirebaseDatabase.getInstance();
                DatabaseReference tempGraphsRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/graphs_temp");
                tempGraphsRef.addListenerForSingleValueEvent(new ValueEventListener() {
                    @Override
                    public void onDataChange(DataSnapshot dataSnapshot) {
                        ArrayList<Bitmap> image_bitmaps = new ArrayList<>();
                        for(DataSnapshot postSnapshot : dataSnapshot.getChildren()){
                            String image_string = postSnapshot.getValue(String.class);

                            byte[] decodedString = Base64.decode(image_string.getBytes(), Base64.DEFAULT);
                            Bitmap image = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
                            image_bitmaps.add(image);
                        }

                        viewPagerAdapter = new ViewPagerAdapter(image_bitmaps, HomeActivity.this);
                        viewPager.setAdapter(viewPagerAdapter);
                    }

                    @Override
                    public void onCancelled(DatabaseError databaseError) {
                        // ...
                    }
                });
            }
        });

        humidityPanel = findViewById(R.id.hum_panel);
        humidityPanel.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                TextView current_temperature_text = findViewById(R.id.current_temperature);
                current_temperature_text.setTextColor(Color.parseColor("#707070"));
                TextView temperature_label_text = findViewById(R.id.temp_label);
                temperature_label_text.setTextColor(Color.parseColor("#707070"));
                TextView current_humidity_text = findViewById(R.id.current_humidity);
                current_humidity_text.setTextColor(Color.parseColor("#000000"));
                TextView humidity_label_text = findViewById(R.id.hum_label);
                humidity_label_text.setTextColor(Color.parseColor("#000000"));
                temp_graphs = false;
                hum_graphs = true;
                FirebaseDatabase database = FirebaseDatabase.getInstance();
                DatabaseReference humGraphsRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/graphs_hum");
                humGraphsRef.addListenerForSingleValueEvent(new ValueEventListener() {
                    @Override
                    public void onDataChange(DataSnapshot dataSnapshot) {
                        ArrayList<Bitmap> image_bitmaps = new ArrayList<>();
                        for(DataSnapshot postSnapshot : dataSnapshot.getChildren()){
                            String image_string = postSnapshot.getValue(String.class);

                            byte[] decodedString = Base64.decode(image_string.getBytes(), Base64.DEFAULT);
                            Bitmap image = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
                            image_bitmaps.add(image);
                        }

                        viewPagerAdapter = new ViewPagerAdapter(image_bitmaps, HomeActivity.this);
                        viewPager.setAdapter(viewPagerAdapter);
                    }

                    @Override
                    public void onCancelled(DatabaseError databaseError) {
                        // ...
                    }
                });

            }
        });

    }

    public void updateStats() {
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference tempRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/current_measurement/temperature");
        DatabaseReference humidRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/current_measurement/humidity");
        DatabaseReference lightRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/current_measurement/light");
        DatabaseReference tempGraphsRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/graphs_temp");
        DatabaseReference humGraphsRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/graphs_hum");
        // Read from the database
        tempRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                String value = Integer.toString((int) Math.round(dataSnapshot.getValue(Double.class)));
                TextView temperature= findViewById(R.id.current_temperature);
                String temp_text = value + "°C";
                temperature.setText(temp_text);
            }

            @Override
            public void onCancelled(DatabaseError error) {
                // Failed to read value
                Log.w(TAG, "Failed to read value.", error.toException());
            }
        });

        humidRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                String value = Integer.toString((int) Math.round(dataSnapshot.getValue(Double.class)));
                TextView humidity= findViewById(R.id.current_humidity);
                String hum_text = value + "%";
                humidity.setText(hum_text);
            }

            @Override
            public void onCancelled(DatabaseError error) {
                // Failed to read value
                Log.w(TAG, "Failed to read value.", error.toException());
            }
        });
        lightRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                String value = Integer.toString((int) Math.round(dataSnapshot.getValue(Double.class)));
                TextView lighting= findViewById(R.id.current_light);
                String light_text = value;
                lighting.setText(light_text);
            }

            @Override
            public void onCancelled(DatabaseError error) {
                // Failed to read value
                Log.w(TAG, "Failed to read value.", error.toException());
            }
        });

        tempGraphsRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                if(temp_graphs){
                    ArrayList<Bitmap> image_bitmaps = new ArrayList<>();
                    for(DataSnapshot postSnapshot : dataSnapshot.getChildren()){
                        String image_string = postSnapshot.getValue(String.class);

                        byte[] decodedString = Base64.decode(image_string.getBytes(), Base64.DEFAULT);
                        Log.w(TAG, image_string);
                        Bitmap image = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
                        if (image == null){
                            Log.w(TAG, "Urine trouble");
                        }
                        Log.w(TAG, "after bitmap factory");
                        image_bitmaps.add(image);
                    }

                    viewPagerAdapter = new ViewPagerAdapter(image_bitmaps, HomeActivity.this);
                    viewPager.setAdapter(viewPagerAdapter);

                }

            }

            @Override
            public void onCancelled(DatabaseError error) {
                // Failed to read value
                Log.w(TAG, "Failed to read value.", error.toException());
            }
        });

        humGraphsRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                if(hum_graphs){
                    ArrayList<Bitmap> image_bitmaps = new ArrayList<>();
                    for(DataSnapshot postSnapshot : dataSnapshot.getChildren()){
                        String image_string = postSnapshot.getValue(String.class);

                        byte[] decodedString = Base64.decode(image_string, Base64.DEFAULT);
                        Bitmap image = BitmapFactory.decodeByteArray(decodedString, 0, decodedString.length);
                        image_bitmaps.add(image);
                    }

                    viewPagerAdapter = new ViewPagerAdapter(image_bitmaps, HomeActivity.this);
                    viewPager.setAdapter(viewPagerAdapter);
                }

            }

            @Override
            public void onCancelled(DatabaseError error) {
                // Failed to read value
                Log.w(TAG, "Failed to read value.", error.toException());
            }
        });
    }

}


