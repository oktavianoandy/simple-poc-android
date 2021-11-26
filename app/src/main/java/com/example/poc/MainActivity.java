package com.example.poc;

import androidx.appcompat.app.AppCompatActivity;
import androidx.databinding.DataBindingUtil;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;
import com.example.poc.databinding.ActivityMainBinding;

import java.io.ByteArrayOutputStream;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.net.URLEncoder;

public class MainActivity extends AppCompatActivity {

    int SELECT_PICTURE1 = 200;
    int SELECT_PICTURE2 = 201;

    String img1String = "";
    String img2String = "";

    ActivityMainBinding binding;
    Bitmap bitmap;
    BitmapDrawable drawable;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = DataBindingUtil.setContentView(this, R.layout.activity_main);
        initPython();

        binding.btImage1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                imageChooser1();
            }
        });

        binding.btImage2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                imageChooser2();
            }
        });

        binding.btProsesPoc.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                binding.tvNilaiPoc.setText(getPOCValue());
            }
        });

    }

    void imageChooser1() {
        Intent i = new Intent();
        i.setType("image/*");
        i.setAction(Intent.ACTION_GET_CONTENT);
        startActivityForResult(Intent.createChooser(i, "Select Picture"), SELECT_PICTURE1);
    }

    void imageChooser2() {
        Intent i = new Intent();
        i.setType("image/*");
        i.setAction(Intent.ACTION_GET_CONTENT);
        startActivityForResult(Intent.createChooser(i, "Select Picture"), SELECT_PICTURE2);
    }

    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == RESULT_OK) {
            Uri selectedImageUri = data.getData();
            if (requestCode == SELECT_PICTURE1) {
                if (null != selectedImageUri) {
                    binding.imgSelected.setImageURI(selectedImageUri);
                    drawable = (BitmapDrawable) binding.imgSelected.getDrawable();
                    bitmap = drawable.getBitmap();
                    img1String = getStringImage(bitmap);
                    Log.i("imgString 1", img1String);
                }
            }else if (requestCode == SELECT_PICTURE2)  {
                if (null != selectedImageUri) {
                    binding.imgSelected.setImageURI(selectedImageUri);
                    drawable = (BitmapDrawable) binding.imgSelected.getDrawable();
                    bitmap = drawable.getBitmap();
                    img2String = getStringImage(bitmap);
                    Log.i("imgString 2", img2String);
                }
            }
        }
    }

    private String getStringImage(Bitmap bitmap) {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.PNG, 100, baos);
        byte[] imageBytes = baos.toByteArray();
        String encodeImage = android.util.Base64.encodeToString(imageBytes, Base64.DEFAULT);
        return encodeImage;
    }

    private void initPython() {
        if (!Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }
    }

    private String getPOCValue() {
        Python python = Python.getInstance();
        PyObject pythonFile = python.getModule("poc");
        if (img1String.equals(img2String)) {
            Toast.makeText(this, "Gambar sama", Toast.LENGTH_SHORT).show();
        } else {
            Toast.makeText(this, "Gambar tidak sama", Toast.LENGTH_SHORT).show();
        }
        return pythonFile.callAttr("nilaiPOC", img1String + ',' + img2String).toString();
    }
}