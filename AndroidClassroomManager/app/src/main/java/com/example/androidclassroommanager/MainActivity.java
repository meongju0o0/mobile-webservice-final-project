package com.example.androidclassroommanager;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {
    private RecyclerView recyclerView;
    private ClassroomPhotoAdapter adapter;
    private ClassroomPhotoApi photoApi;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        recyclerView = findViewById(R.id.recyclerView);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));

        String token = getToken();
        if (token == null) {
            startActivity(new Intent(this, LoginActivity.class));
            finish();
            return;
        }

        loadClassroomPhotos(token);
    }

    private void loadClassroomPhotos(String token) {
        RetrofitClient.getClient()
                .create(ClassroomPhotoApi.class)
                .getClassroomPhotos("Token " + token)
                .enqueue(new Callback<List<ClassroomPhoto>>() {
                    @Override
                    public void onResponse(Call<List<ClassroomPhoto>> call, Response<List<ClassroomPhoto>> response) {
                        if (response.isSuccessful() && response.body() != null) {
                            List<ClassroomPhoto> photos = response.body();
                            adapter = new ClassroomPhotoAdapter(photos);
                            recyclerView.setAdapter(adapter);
                        } else {
                            Log.e("MainActivity", "사진 가져오기 실패: " + response.code());
                        }
                    }

                    @Override
                    public void onFailure(Call<List<ClassroomPhoto>> call, Throwable t) {
                        Log.e("MainActivity", "API 요청 실패: " + t.getMessage());
                    }
                });
    }

    private String getToken() {
        SharedPreferences prefs = getSharedPreferences("AppPrefs", MODE_PRIVATE);
        return prefs.getString("token", null);
    }
}
