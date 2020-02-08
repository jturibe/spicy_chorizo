package com.example.particle;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import static android.content.ContentValues.TAG;

public class HomeActivity extends Activity {

    public void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);
        basicReadWrite();
    }

    public void basicReadWrite() {
        // [START write_message]
        // Write a message to the database
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        DatabaseReference tempRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/current_measurement/temperature");
        DatabaseReference humidRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/current_measurement/humidity");
        DatabaseReference lightRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/current_measurement/light");
        // [START read_message]
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

    }

}
