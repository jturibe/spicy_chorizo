package com.example.particle;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.TextView;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import static android.content.ContentValues.TAG;

public class displaySettings extends Activity {

    Button editButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_display_settings);

        updateStats();

        editButton = findViewById(R.id.editButton);
        editButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(displaySettings.this, editSettings.class);
                startActivity(intent);
            }
        });
    }

    private void updateStats() {
        FirebaseDatabase database = FirebaseDatabase.getInstance();

        DatabaseReference tempMaxRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/user_settings/temperature_max");
        DatabaseReference tempMinRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/user_settings/temperature_min");
        DatabaseReference humMinRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/user_settings/humidity_min");
        DatabaseReference humMaxRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/user_settings/humidity_max");

        tempMaxRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                String value = Integer.toString((int) Math.round(dataSnapshot.getValue(Double.class)));
                TextView temperature= findViewById(R.id.temp_max);
                String temp_text = value;
                temperature.setText(temp_text);
            }

            @Override
            public void onCancelled(DatabaseError error) {
                // Failed to read value
                Log.w(TAG, "Failed to read value.", error.toException());
            }
        });

        tempMinRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                String value = Integer.toString((int) Math.round(dataSnapshot.getValue(Double.class)));
                TextView temperature= findViewById(R.id.temp_min);
                String temp_text = value;
                temperature.setText(temp_text);
            }

            @Override
            public void onCancelled(DatabaseError error) {
                // Failed to read value
                Log.w(TAG, "Failed to read value.", error.toException());
            }
        });

        humMaxRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                String value = Integer.toString((int) Math.round(dataSnapshot.getValue(Double.class)));
                TextView humidity = findViewById(R.id.hum_max);
                String hum_text = value;
                humidity.setText(hum_text);
            }

            @Override
            public void onCancelled(DatabaseError error) {
                // Failed to read value
                Log.w(TAG, "Failed to read value.", error.toException());
            }
        });

        humMinRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                // This method is called once with the initial value and again
                // whenever data at this location is updated.
                String value = Integer.toString((int) Math.round(dataSnapshot.getValue(Double.class)));
                TextView humidity = findViewById(R.id.hum_min);
                String hum_text = value;
                humidity.setText(hum_text);
            }

            @Override
            public void onCancelled(DatabaseError error) {
                // Failed to read value
                Log.w(TAG, "Failed to read value.", error.toException());
            }
        });

    }
}
