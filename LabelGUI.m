% This file was produced by matlab's GUI IDE "GUIDE." Most of the
% functions in come from that.
function varargout = LabelGUI(varargin)
% LABELGUI MATLAB code for LabelGUI.fig
%      LABELGUI, by itself, creates a new LABELGUI or raises the existing
%      singleton*.
%
%      H = LABELGUI returns the handle to a new LABELGUI or the handle to
%      the existing singleton*.
%
%      LABELGUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in LABELGUI.M with the given input arguments.
%
%      LABELGUI('Property','Value',...) creates a new LABELGUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before LabelGUI_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to LabelGUI_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help LabelGUI

% Last Modified by GUIDE v2.5 29-Nov-2012 10:01:15

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @LabelGUI_OpeningFcn, ...
                   'gui_OutputFcn',  @LabelGUI_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before LabelGUI is made visible.
function LabelGUI_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to LabelGUI (see VARARGIN)

% The following three variables store information that is crucial
% to the displaying of the proper graph. whichFrame dictates which
% frame to produce, index which cell and ch which channel.
handles.whichFrame = 1;
handles.index = 1;
handles.ch = 1;
handles.t = -1;

% Loading in the data
tcMatFile = './data/020512_hCD8/nveMemDonA_020512_v2_results.mat';
outputCell = load([tcMatFile]);
trackCount = length(outputCell.datacell);
handles.outputCell = outputCell.datacell;
% will be made into a string for the cell track list
trackID = 1:trackCount;

% xPos and yPos define the position of the box that follows the
% selected cell tracks. This function is only called when the GUI
% is initialized, so it loads the positions of the first cell track
handles.xPos = handles.outputCell{handles.index}(:,3);
handles.yPos = handles.outputCell{handles.index}(:,4);
handles.startFrame = handles.outputCell{handles.index}(1,1);
handles.endFrame = handles.outputCell{handles.index}(1,2);

% The names of the pictures for the two channels that will be
% loaded into the GUI
ch1PicNames = dir(fullfile(pwd,'data','020512_hCD8','nveMemDonA','*_c001.jpg'));
ch2PicNames = dir(fullfile(pwd,'data','020512_hCD8','nveMemDonA','*_c004.jpg'));

handles.manyFrames = length(ch1PicNames);

handles.sf = handles.startFrame/handles.manyFrames;

% Loads in pictures
for i = 1:handles.manyFrames
    handles.images{1,i} = imread(fullfile(...
        'data','020512_hCD8','nveMemDonA',ch1PicNames(i).name));
    handles.images{1,i} = imresize(...
        handles.images{1,i}, [225 225]);
    handles.images{2,i} = imread(fullfile(...
        'data','020512_hCD8','nveMemDonA',ch2PicNames(i).name));
    handles.images{2,i} = imresize(...
        handles.images{2,i}, [225 225]);
end

handles.types = cell(trackCount);
handles.types{handles.index} = zeros(length(handles.xPos),1)-1;

% Loads the position of 
set(handles.positions,'Data',[handles.xPos,handles.yPos,handles.types{handles.index}]);

% Loads the numbers of the cell tracks into the right-most pannel
% that the user clicks to select 
set(handles.cellTrack,'string',trackID);

% Choose default command line output for LabelGUI
handles.output = hObject;

% Loads the text into the little 
frameInfoText(handles);
%makePlot(handles);

set(handles.cellTrack,'Value',handles.index);
cellTrack_Callback(handles.cellTrack, eventdata, handles)

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes LabelGUI wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = LabelGUI_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on slider movement.
function frameSlider_Callback(hObject, eventdata, handles)
% hObject    handle to frameSlider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% maps the frame slider position to an equivalent frame
handles.whichFrame = floor(get(hObject,'Value')*(handles.manyFrames-1))+1;

% fills in the information pannel that displays the current frame
% as well as when the selected cell track starts and stops
frameInfoText(handles);
% Graphs the pictures, bounding box, and trajectory
makePlot(handles);
guidata(hObject, handles);

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes during object creation, after setting all properties.
function frameSlider_CreateFcn(hObject, eventdata, handles)
% hObject    handle to frameSlider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% The left-most panel that let's the user select which cell track
% --- Executes on selection change in cellTrack.
function cellTrack_Callback(hObject, eventdata, handles)
% hObject    handle to cellTrack (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

handles.index = get(hObject,'Value');

handles.xPos = handles.outputCell{handles.index}(:,3);
handles.yPos = handles.outputCell{handles.index}(:,4);
handles.startFrame = handles.outputCell{handles.index}(1,1);
handles.endFrame = handles.outputCell{handles.index}(1,2);

handles.sf = handles.startFrame/handles.manyFrames;
if (isempty(handles.types{handles.index}))
    handles.types{handles.index} = zeros(length(handles.xPos),1)-1;
end

set(handles.positions,'Data',[handles.xPos,handles.yPos,handles.types{handles.index}]);
set(handles.frameSlider,'Value',handles.sf);
guidata(hObject, handles);

if ~((get(handles.playButton,'Value')))
    frameSlider_Callback(handles.frameSlider,[],handles);
else
    set(handles.playButton,'Value',0);
    playButton_Callback(handles.playButton,[],handles)
end


% Hints: contents = cellstr(get(hObject,'String')) returns cellTrack contents as cell array
%        contents{get(hObject,'Value')} returns selected item from cellTrack


% --- Executes during object creation, after setting all properties.
function cellTrack_CreateFcn(hObject, eventdata, handles)
% hObject    handle to cellTrack (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: listbox controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes during object creation, after setting all properties.
function positions_CreateFcn(hObject, eventdata, handles)
% hObject    handle to positions (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called


% --- Executes when selected object is changed in uipanel1.
function uipanel1_SelectionChangeFcn(hObject, eventdata, handles)
% hObject    handle to the selected object in uipanel1 
% eventdata  structure with the following fields (see UIBUTTONGROUP)
%	EventName: string 'SelectionChanged' (read only)
%	OldValue: handle of the previously selected object or empty if none was selected
%	NewValue: handle of the currently selected object
% handles    structure with handles and user data (see GUIDATA)

switch handles.ch
  case 1
    handles.ch = 2;
  case 2
    handles.ch = 1;
end

guidata(hObject, handles);

if ~((get(handles.playButton,'Value')))
    makePlot(handles);
else
    set(handles.playButton,'Value',0);
    playButton_Callback(handles.playButton,[],handles)
    set(handles.playButton,'Value',1);
    playButton_Callback(handles.playButton,[],handles)
end


% --- Executes on button press in playButton.
function playButton_Callback(hObject, eventdata, handles)
% hObject    handle to playButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

handles.whichFrame = floor(get(handles.frameSlider,'Value')*(handles.manyFrames-1))+1;
trackLen = handles.endFrame-handles.startFrame+1;
startPlay = get(handles.frameSlider,'Value');
%startPlay = handles.whichFrame/handles.manyFrames;
%set(handles.frameSlider,'Value',startPlay);
%frameSlider_Callback(handles.frameSlider,[],handles);

if ((handles.whichFrame > handles.endFrame) | ...
    (startPlay < handles.sf))
    startPlay = handles.sf;
end

i = 0;
while get(hObject,'Value')
    % Edits cell type

    if ((i == 0) & ...
        (handles.types{handles.index}(handles.whichFrame-handles.startFrame+1) ...
         ~= -1))
        handles.t = handles.types{handles.index}(handles.whichFrame-handles.startFrame+1);
    end
    handles.types{handles.index}(handles.whichFrame-handles.startFrame+1) = ...
    positions_CellEditCallback(handles.positions, ...
                               struct( ...
                                   'Indices',[handles.whichFrame,3], ...
                                   'EditData',num2str(handles.t),'NewData',handles.t,'Error',[],...
                                   'PreviousData',...
                                   handles.types{handles.index}...
                                   (handles.whichFrame-handles.startFrame+1)),... 
                               handles);

    % This next chunk deals with moving the slider and playing the
    % video correctly
    % handles.sf is just startFrame/manyFrames--just a term I made
    % a variable to reduce clutter
    set(handles.frameSlider,'Value', ...
                      (mod(1000.*(startPlay-handles.sf+i/handles.manyFrames), ...
                           trackLen*1000./handles.manyFrames)...
                       +(handles.sf)*1000.)/1000.);
    frameSlider_Callback(handles.frameSlider,[],handles);
    handles.whichFrame = floor(get(handles.frameSlider,'Value')*(handles.manyFrames-1))+1;
    %{
    disp('new round')
    handles.whichFrame-handles.startFrame+1
    handles.whichFrame
    %}
    guidata(hObject, handles);
    set(handles.positions,'Data',[handles.xPos,handles.yPos,handles.types{handles.index}]);
    pause(.2);
    i = i+1;
end

% Hint: get(hObject,'Value') returns toggle state of playButton


% --- Executes when entered data in editable cell(s) in positions.
function ctypes = positions_CellEditCallback(hObject, eventdata, handles)
% hObject    handle to positions (see GCBO)
% eventdata  structure with the following fields (see UITABLE)
%	Indices: row and column indices of the cell(s) edited
%	PreviousData: previous data for the cell(s) edited
%	EditData: string(s) entered by the user
%	NewData: EditData or its converted form set on the Data property. Empty if Data was not changed
%	Error: error string when failed to convert EditData to appropriate value for Data
% handles    structure with handles and user data (see GUIDATA)

handles.types{handles.index}(eventdata.Indices(1)) = eventdata.NewData;
guidata(hObject, handles);

ctypes = handles.types{handles.index}(eventdata.Indices(1));

% --- Executes on button press in switchType.
function switchType_Callback(hObject, eventdata, handles)
% hObject    handle to switchType (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
switch handles.t
  case 0
    handles.t = 1;
  case 1
    handles.t = 0;
  otherwise
    handles.t = -1;
end

guidata(hObject, handles);

if ((get(handles.playButton,'Value')))
    set(handles.playButton,'Value',0);
    playButton_Callback(handles.playButton,[],handles)
    set(handles.playButton,'Value',1);
    playButton_Callback(handles.playButton,[],handles)
end


% --- Executes on button press in saveTypes.
function saveTypes_Callback(hObject, eventdata, handles)
% hObject    handle to saveTypes (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

savefile = 'memDonAclass.mat';
save(savefile,'handles.types');


% --- Executes during object creation, after setting all properties.
function frameInfo_CreateFcn(hObject, eventdata, handles)
% hObject    handle to frameInfo (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called


% --- Executes on key press with focus on playButton and none of its controls.
function playButton_KeyPressFcn(hObject, eventdata, handles)
% hObject    handle to playButton (see GCBO)
% eventdata  structure with the following fields (see UICONTROL)
%	Key: name of the key that was pressed, in lower case
%	Character: character interpretation of the key(s) that was pressed
%	Modifier: name(s) of the modifier key(s) (i.e., control, shift) pressed
% handles    structure with handles and user data (see GUIDATA)


% --- Executes when selected cell(s) is changed in positions.
function positions_CellSelectionCallback(hObject, eventdata, handles)
% hObject    handle to positions (see GCBO)
% eventdata  structure with the following fields (see UITABLE)
%	Indices: row and column indices of the cell(s) currently selecteds
% handles    structure with handles and user data (see GUIDATA)


% --- If Enable == 'on', executes on mouse press in 5 pixel border.
% --- Otherwise, executes on mouse press in 5 pixel border or over playButton.
function playButton_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to playButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Makes plots.
function makePlot(handles)
imagesc(handles.images{handles.ch,handles.whichFrame});
hold on;
axis([0 225 0 225])
axis square;
if ((handles.whichFrame >= handles.startFrame) & ...
    (handles.whichFrame <= handles.endFrame))
    plot(handles.xPos,handles.yPos);
    rectangle('Position',[handles.xPos(handles.whichFrame-handles.startFrame+1)-5, ...
                        handles.yPos(handles.whichFrame-handles.startFrame+1)-5,10,10], ... 
              'EdgeColor','g','LineStyle',':');
end
set(gca,'XTick',[]);
set(gca,'YTick',[]);
hold off;

% --- Makes the text that describes the current frame as well as
% the start frame and end frame for the selected cell track.
function frameInfoText(handles)
toPrint = sprintf('Frame: %i\nStart: %i\nEnd: %i', ...
                  handles.whichFrame,handles.startFrame,handles.endFrame);
set(handles.frameInfo,'String',toPrint);
