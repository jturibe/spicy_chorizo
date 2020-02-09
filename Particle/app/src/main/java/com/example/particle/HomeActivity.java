package com.example.particle;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.viewpager.widget.ViewPager;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.google.firebase.messaging.FirebaseMessaging;

import static android.content.ContentValues.TAG;

public class HomeActivity extends Activity {

    ImageButton settingsButton;
    ViewPager viewPager;

    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);
        FirebaseMessaging.getInstance().subscribeToTopic("emergency_updates");
        updateStats();
        settingsButton = findViewById(R.id.settingsButton);
        settingsButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(HomeActivity.this, displaySettings.class);
                startActivity(intent);
            }
        });

        viewPager = (ViewPager) findViewById(R.id.viewPager);

        ViewPagerAdapter viewPagerAdapter = new ViewPagerAdapter(this);

        viewPager.setAdapter(viewPagerAdapter);

    }

    public void updateStats() {
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference tempRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/current_measurement/temperature");
        DatabaseReference humidRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/current_measurement/humidity");
        DatabaseReference lightRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/current_measurement/light");
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
    }

}


