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

                if (minTempInputFinal<4) {
                    AlertDialog.Builder minTempTooLow = new AlertDialog.Builder(editSettings.this);
                    minTempTooLow.setMessage("The minimum temperature set is dangerously low, " +
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
