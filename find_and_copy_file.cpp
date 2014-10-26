#include "stdafx.h"
#include "find_and_copy_file.h"

#include <string>
#include <fstream>
#include <set>

#ifdef WIN32
#include <Windows.h>
#endif // WIN32

using namespace std;

struct SearchInfo
{
	SearchInfo() : _isFound(false) {}
	SearchInfo(const string& fileName, bool isFound = false)
		: _fileName(fileName), _isFound(isFound) {}
	bool operator<(const SearchInfo& rhs) const
	{
		return _fileName < rhs._fileName;
	}

	string _fileName;
	bool _isFound;
};

void EnsureDirExsist(const char* pDir)
{
	WIN32_FIND_DATAA findData;
	HANDLE hFoundDir = FindFirstFileA(pDir, &findData);
	if (hFoundDir == INVALID_HANDLE_VALUE)
	{
		BOOL successful = CreateDirectoryA(pDir, NULL);
		assert(successful);
	}
	else
		FindClose(hFoundDir);
}

int FindFilesInDir(set<SearchInfo>& fileInfos, const char* pSrcDir, const char* pDestDir)
{
	WIN32_FIND_DATAA data;
	int i = 0;
	string fileNameMode(pSrcDir);
	fileNameMode += "/*";
	HANDLE hFoundFile = FindFirstFileA(fileNameMode.c_str(), &data);
	while (hFoundFile != INVALID_HANDLE_VALUE && FindNextFileA(hFoundFile, &data)) 
	{		
		if (!strcmp(data.cFileName, "..") || !strcmp(data.cFileName, "."))
			continue;

		if (data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
		{
			string subDir(pSrcDir);
			subDir += '/';
			subDir += data.cFileName;
			i += FindFilesInDir(fileInfos, subDir.c_str(), pDestDir);
		}
		else
		{
			string currFileName = data.cFileName;
			set<SearchInfo>::iterator iter = fileInfos.find(currFileName);
			if (iter != fileInfos.end())
			{
				i++;
				bool(iter->_isFound) = true;
// 				fileInfos.erase(iter);
// 				fileInfos.insert(SearchInfo(currFileName, true));
				string fileDir(pSrcDir);
				fileDir += '/';
				fileDir += currFileName;
				string destFileDir(pDestDir);
				destFileDir += '/';
				destFileDir += currFileName;
				EnsureDirExsist(pDestDir);
				BOOL successful = CopyFileA(fileDir.c_str(), destFileDir.c_str(), FALSE);
				assert(successful);
			}
		}
	}
	FindClose(hFoundFile);
	return i;
}

void FindAndCopyFile(const char* pFile, const char* pSearchDir, const char* pDestDir)
{
	cout << "input a file contain files' name:" << endl;
	string fileName("C:/Users/chenjiahong/Desktop/files.txt");
// 	if (!pFile)
// 		cin >> fileName;
	cout << "input a directory to search:" << endl;
	string searchDir("C:/Users/chenjiahong/Desktop/samples");
// 	if (!pSearchDir)
// 		cin >> searchDir;
	cout << "input a directory to save found files:" << endl;
	string destDir("c:/foundFile");
// 	if (!pDestDir)
// 		cin >> destDir;
	set<SearchInfo> fileInfos;
	ifstream file(fileName, ios_base::in);
	int foundCount = 0;
	if (file)
	{
		string currName;
		while (getline(file, currName))
		{
			size_t dirFlag = currName.find_last_of("\\/");
			if (dirFlag != string::npos)
				currName = currName.substr(dirFlag + 1, currName.size() - dirFlag + 1);
			fileInfos.insert(currName);
		}
		foundCount = FindFilesInDir(fileInfos, searchDir.c_str(), destDir.c_str());
	}
	cout << fileInfos.size() << " files in all, and "
		<< foundCount << " found! (miss files show below)" << endl;
	for (auto iter = fileInfos.begin(); iter != fileInfos.end(); ++iter)
	{
		if (!iter->_isFound)
			cout << iter->_fileName << endl;
	}
}