package com.example.androidclassroommanager;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.engine.DiskCacheStrategy;

import java.util.List;

public class ClassroomPhotoAdapter extends RecyclerView.Adapter<ClassroomPhotoAdapter.ViewHolder> {
    private List<ClassroomPhoto> photos;

    public ClassroomPhotoAdapter(List<ClassroomPhoto> photos) {
        this.photos = photos;
    }

    @NonNull
    @Override
    public ClassroomPhotoAdapter.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_classroom_photo, parent, false);
        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        ClassroomPhoto photo = photos.get(position);
        holder.peopleCount.setText("Number of people: " + photo.getNumber_of_people());
        holder.uploadedAt.setText("Uploaded at: " + photo.getUploaded_at());

        String imageUrl = "https://meongju0o0.pythonanywhere.com" + photo.getImage();
        Glide.with(holder.itemView.getContext())
                .load(imageUrl)
                .placeholder(R.drawable.placeholder_image)
                .error(R.drawable.error_image)
                .diskCacheStrategy(DiskCacheStrategy.ALL)
                .into(holder.imageView);
    }

    @Override
    public int getItemCount() {
        return photos.size();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        ImageView imageView;
        TextView peopleCount;
        TextView uploadedAt;

        public ViewHolder(@NonNull View itemView) {
            super(itemView);
            imageView = itemView.findViewById(R.id.photoImageView);
            peopleCount = itemView.findViewById(R.id.peopleCountTextView);
            uploadedAt = itemView.findViewById(R.id.uploadedAtTextView);
        }
    }
}
