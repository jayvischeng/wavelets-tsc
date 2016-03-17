figure()

[phi, psi, xval] = wavefun('haar');
subplot(131);
plot(xval, psi,'LineWidth',1);
xlim([-0.1 1.1])
title('Haar');

% figure;
[phi, psi, xval] = wavefun('db20');
subplot(132);
plot(xval, psi,'LineWidth',1);
title('Daubechies 20');
% saveas(gcf, '~/Documents/Papers/2016.02.SEKE/fig/db20.eps', 'eps2c')

% figure;
[phi, psi, xval] = wavefun('sym20');
subplot(133);
plot(xval, psi,'LineWidth',1);
title('Symlets 20');

set(gcf, 'PaperUnits', 'centimeters');
set(gcf, 'PaperPosition', [0 0 20 7]); %x_width=10cm y_width=15cm
saveas(gcf, '~/Documents/Papers/2016.02.SEKE/fig/wavefun.eps', 'eps2c')
