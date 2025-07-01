#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

void write_result(FILE *outFile, const char *path) {
    fprintf(outFile, "%s\n", path);
}

void search_directory(FILE *outFile, const char *directory, const char *filename) {
    char path[MAX_PATH];
    WIN32_FIND_DATAA findData;
    HANDLE hFind;

    snprintf(path, MAX_PATH, "%s\\*", directory);
    hFind = FindFirstFileA(path, &findData);

    if (hFind == INVALID_HANDLE_VALUE) return;

    do {
        if (strcmp(findData.cFileName, ".") == 0 || strcmp(findData.cFileName, "..") == 0)
            continue;

        char fullPath[MAX_PATH];
        snprintf(fullPath, MAX_PATH, "%s\\%s", directory, findData.cFileName);

        if (findData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
            search_directory(outFile, fullPath, filename);
        } else {
            if (strstr(findData.cFileName, filename)) {
                write_result(outFile, fullPath);
            }
        }

    } while (FindNextFileA(hFind, &findData));
    FindClose(hFind);
}

void search_all_drives(FILE *outFile, const char *filename) {
    DWORD drives = GetLogicalDrives();
    char root[4] = "A:\\";

    for (int i = 0; i < 26; i++) {
        if (drives & (1 << i)) {
            root[0] = 'A' + i;
            UINT type = GetDriveTypeA(root);
            if (type == DRIVE_FIXED || type == DRIVE_REMOVABLE) {
                search_directory(outFile, root, filename);
            }
        }
    }
}

int main() {
    FILE *searchFile = fopen("search.bin", "r");
    if (!searchFile) {
        fprintf(stderr, "Failed to open search.bin\n");
        return 1;
    }

    char filename[256], directory[512];
    fgets(filename, sizeof(filename), searchFile);
    fgets(directory, sizeof(directory), searchFile);
    fclose(searchFile);

    // Strip newline characters
    filename[strcspn(filename, "\r\n")] = '\0';
    directory[strcspn(directory, "\r\n")] = '\0';

    FILE *outFile = fopen("searched.bin", "w");
    if (!outFile) {
        fprintf(stderr, "Failed to open searched.bin for writing\n");
        return 1;
    }

    if (strlen(directory) == 0) {
        search_all_drives(outFile, filename);
    } else {
        search_directory(outFile, directory, filename);
    }

    fclose(outFile);
    return 0;
}
