package com.example.particle;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class editSettings extends Activity {

    EditText editTextMinTemp;
    EditText editTextMaxTemp;
    EditText editTextMinHum;
    EditText editTextMaxHum;

    Button submitButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_edit_settings);

        editTextMinTemp = findViewById(R.id.minTempInput);
        editTextMaxTemp = findViewById(R.id.maxTempInput);
        editTextMinHum = findViewById(R.id.minHumInput);
        editTextMaxHum = findViewById(R.id.maxHumInput);

        submitButton = findViewById(R.id.submitButton);

        editTextMinTemp.addTextChangedListener(data);
        editTextMaxTemp.addTextChangedListener(data);
        editTextMinHum.addTextChangedListener(data);
        editTextMaxHum.addTextChangedListener(data);

        submitButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                String minTempInputint= editTextMinTemp.getText().toString();
                int minTempInputFinal = Integer.parseInt(minTempInputint);
                String maxTempInputint= editTextMaxTemp.getText().toString();
                int maxTempInputFinal = Integer.parseInt(maxTempInputint);
                String minHumInputint= editTextMinHum.getText().toString();
                int minHumInputFinal = Integer.parseInt(minHumInputint);
                String maxHumInputint= editTextMaxHum.getText().toString();
                int maxHumInputFinal = Integer.parseInt(maxHumInputint);

                if (minTempInputFinal<0 || maxTempInputFinal > 26 || minHumInputFinal < 50 || maxHumInputFinal > 80) {
                    AlertDialog.Builder minTempTooLow = new AlertDialog.Builder(editSettings.this);
                    minTempTooLow.setMessage("One of the settings is dangerously high/low, " +
                            "do you want to change it?")
                            .setPositiveButton("No",
                                    new DialogInterface.OnClickListener() {
                                        public void onClick(DialogInterface dialog, int whichButton) {
                                            positiveButtonPress();
                                        }
                                    })
                            .setNegativeButton("Yes", null);
                    AlertDialog alert = minTempTooLow.create();
                    alert.show();
                } else {
                    FirebaseDatabase database = FirebaseDatabase.getInstance();

                    DatabaseReference tempMaxRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/user_settings/temperature_max");
                    DatabaseReference tempMinRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/user_settings/temperature_min");
                    DatabaseReference humMinRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/user_settings/humidity_min");
                    DatabaseReference humMaxRef = database.getReferenceFromUrl("https://spicychorizo-794f1.firebaseio.com/user_settings/humidity_max");

                    tempMaxRef.setValue(Double.parseDouble(editTextMaxTemp.getText().toString()));
                    tempMinRef.setValue(Double.parseDouble(editTextMinTemp.getText().toString()));
                    humMaxRef.setValue(Double.parseDouble(editTextMaxHum.getText().toString()));
                    humMinRef.setValue(Double.parseDouble(editTextMinHum.getText().toString()));


                    positiveButtonPress();
                }
            }
        });
    }

    private TextWatcher data = new TextWatcher() {
        @Override
        public void beforeTextChanged(CharSequence s, int start, int count, int after) {

        }

        @Override
        public void onTextChanged(CharSequence s, int start, int before, int count) {
            String minTempInput = editTextMinTemp.getText().toString().trim();
            String maxTempInput = editTextMaxTemp.getText().toString().trim();
            String minHumInput = editTextMinHum.getText().toString().trim();
            String maxHumInput = editTextMaxHum.getText().toString().trim();

            submitButton.setEnabled(
                    !minTempInput.isEmpty() && !maxTempInput.isEmpty() &&
                            !minHumInput.isEmpty() && !maxHumInput.isEmpty());
        }

        @Override
        public void afterTextChanged(Editable s) {

        }
    };

    private void positiveButtonPress() {
        Toast.makeText(getBaseContext(), "Settings changed" , Toast.LENGTH_SHORT ).show();
        Intent intent = new Intent(editSettings.this, HomeActivity.class);
        startActivity(intent);
    }
}
