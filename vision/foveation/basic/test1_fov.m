img = imread('test1.png');
%imshow(img)

M = img;
n = size(img,1);



m = 41; % width of filers
p = 20; % number of filters
sigma = linspace(0.05,10,p);
H = zeros(m,m,p);
for i=1:p
    H(:,:,i) = compute_gaussian_filter([m m],sigma(i)/size(img,1),[size(img,1) size(img,2)]);
end

x = linspace(-1,1,n);
[Y,X] = meshgrid(x,x);
R = sqrt(X.^2 + Y.^2);
I = round(rescale(R,1,p));

M1 = perform_adaptive_filtering(M,H,I);
imageplot({M M1},{'Original' 'Foveated'});